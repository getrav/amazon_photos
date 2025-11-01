#!/usr/bin/env python3
"""
Amazon Photos Downloader - Web Server

This is a Flask-based web server that provides a browser interface
for downloading photos from Amazon Photos.

Usage:
    python server.py

Then open your browser to http://localhost:5000
"""

import asyncio
import json
import os
import threading
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from amazon_photos import AmazonPhotos

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Global variables
ap_instance = None
download_in_progress = False
should_stop = False

@app.route('/')
def index():
    """Serve the frontend HTML"""
    return send_from_directory('.', 'frontend.html')

@app.route('/api/validate-cookies', methods=['POST'])
def validate_cookies():
    """Validate Amazon Photos cookies"""
    global ap_instance

    try:
        data = request.get_json()
        cookies = data.get('cookies', {})

        if not cookies:
            return jsonify({'valid': False, 'error': 'No cookies provided'})

        # Try to initialize Amazon Photos with the provided cookies
        ap_instance = AmazonPhotos(
            cookies=cookies,
            tmp='tmp',
        )

        # Try to get usage stats to verify cookies work
        usage = ap_instance.usage()

        return jsonify({
            'valid': True,
            'message': 'Cookies validated successfully!',
            'usage': usage.to_dict('records')
        })

    except Exception as e:
        return jsonify({
            'valid': False,
            'error': str(e)
        })

@app.route('/api/start-download', methods=['POST'])
def start_download():
    """Start downloading all photos"""
    global download_in_progress, should_stop, ap_instance

    if download_in_progress:
        return jsonify({'success': False, 'error': 'Download already in progress'})

    if ap_instance is None:
        return jsonify({'success': False, 'error': 'Please validate cookies first'})

    try:
        data = request.get_json()
        download_path = data.get('path', './downloads')

        # Reset stop flag
        should_stop = False

        # Start download in a separate thread
        thread = threading.Thread(
            target=download_worker,
            args=(download_path,)
        )
        thread.start()

        return jsonify({'success': True, 'message': 'Download started'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/stop-download', methods=['POST'])
def stop_download():
    """Stop the current download"""
    global should_stop
    should_stop = True
    return jsonify({'success': True, 'message': 'Download will stop soon'})

@app.route('/api/gallery', methods=['GET'])
def get_gallery():
    """Get list of downloaded photos for gallery"""
    try:
        download_path = Path('./downloads')

        if not download_path.exists():
            return jsonify({'photos': []})

        photos = []
        for file in download_path.glob('*'):
            if file.is_file() and file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
                photos.append({
                    'name': file.name,
                    'size': file.stat().st_size,
                    'path': str(file.relative_to('.')),
                })

        return jsonify({'photos': photos[:100]})  # Limit to 100 for performance

    except Exception as e:
        return jsonify({'photos': [], 'error': str(e)})

def download_worker(download_path):
    """Worker function that runs the download in a separate thread"""
    global download_in_progress, should_stop, ap_instance

    download_in_progress = True

    try:
        # Emit status update
        socketio.emit('status', {
            'stage': 'fetching',
            'message': 'Fetching your photo library...'
        })

        # Query all photos and videos
        nodes = ap_instance.query("type:(PHOTOS OR VIDEOS)")
        total_items = len(nodes)

        socketio.emit('status', {
            'stage': 'downloading',
            'message': f'Found {total_items:,} items. Starting download...'
        })

        # Create download directory
        Path(download_path).mkdir(parents=True, exist_ok=True)

        # Download in batches to provide progress updates
        batch_size = 100
        downloaded = 0
        errors = []

        for i in range(0, total_items, batch_size):
            if should_stop:
                socketio.emit('status', {
                    'stage': 'stopped',
                    'message': 'Download stopped by user'
                })
                break

            batch = nodes.id[i:i+batch_size]

            try:
                ap_instance.download(batch, out=download_path)
                downloaded += len(batch)

                # Emit progress
                progress = (downloaded / total_items) * 100
                socketio.emit('progress', {
                    'current': f'Batch {i//batch_size + 1} of {(total_items + batch_size - 1)//batch_size}',
                    'progress': progress,
                    'downloaded': downloaded,
                    'total': total_items
                })

            except Exception as e:
                errors.append(str(e))

        # Emit completion
        if not should_stop:
            socketio.emit('complete', {
                'message': f'Download complete! Downloaded {downloaded:,} items.',
                'downloaded': downloaded,
                'errors': errors
            })

    except Exception as e:
        socketio.emit('error', {
            'message': f'Download failed: {str(e)}'
        })

    finally:
        download_in_progress = False

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    emit('status', {'stage': 'connected', 'message': 'Connected to server'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    pass

if __name__ == '__main__':
    print("=" * 70)
    print("Amazon Photos Downloader - Web Server")
    print("=" * 70)
    print("\nServer starting...")
    print("\nOpen your browser to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 70)

    # Create necessary directories
    Path('tmp').mkdir(exist_ok=True)
    Path('downloads').mkdir(exist_ok=True)

    # Run the server
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
