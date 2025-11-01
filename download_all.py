#!/usr/bin/env python3
"""
Amazon Photos Bulk Downloader

This script downloads ALL your photos and videos from Amazon Photos.

Usage:
    python download_all.py

You'll be prompted to enter your cookies, or you can set them as environment variables.
"""

import sys
from pathlib import Path
from amazon_photos import AmazonPhotos

def get_cookies():
    """
    Get cookies from user input.
    Supports US, Canada, and European regions.
    """
    print("=" * 70)
    print("Amazon Photos Bulk Downloader")
    print("=" * 70)
    print("\nTo get your cookies:")
    print("1. Log in to Amazon Photos in your browser")
    print("2. Press F12 to open Developer Tools")
    print("3. Go to 'Application' tab (Chrome) or 'Storage' tab (Firefox)")
    print("4. Find 'Cookies' under your Amazon domain")
    print("5. Copy the values for the cookies listed below\n")

    print("Which region are you in?")
    print("1. United States (.com)")
    print("2. Canada (.ca)")
    print("3. Europe (other)")

    choice = input("\nEnter your choice (1-3): ").strip()

    cookies = {}
    cookies['session-id'] = input("\nEnter 'session-id' cookie value: ").strip()

    if choice == '1':
        # United States
        cookies['ubid-main'] = input("Enter 'ubid-main' cookie value: ").strip()
        cookies['at-main'] = input("Enter 'at-main' cookie value: ").strip()
    elif choice == '2':
        # Canada
        cookies['ubid-acbca'] = input("Enter 'ubid-acbca' cookie value: ").strip()
        cookies['at-acbca'] = input("Enter 'at-acbca' cookie value: ").strip()
    else:
        # Europe
        tld = input("Enter your country TLD (e.g., 'de' for Germany, 'uk' for UK, 'fr' for France): ").strip()
        cookies[f'ubid-acb{tld}'] = input(f"Enter 'ubid-acb{tld}' cookie value: ").strip()
        cookies[f'at-acb{tld}'] = input(f"Enter 'at-acb{tld}' cookie value: ").strip()

    return cookies

def download_all_photos():
    """
    Main function to download all photos from Amazon Photos.
    """
    try:
        # Get cookies from user
        cookies = get_cookies()

        # Initialize Amazon Photos API
        print("\n" + "=" * 70)
        print("Connecting to Amazon Photos...")
        print("=" * 70)

        ap = AmazonPhotos(
            cookies=cookies,
            tmp='tmp',  # Cache responses in tmp folder
        )

        # Show usage stats
        print("\nFetching your Amazon Photos library information...")
        usage = ap.usage()
        print("\nYour Amazon Photos Library:")
        print(usage.to_string(index=False))

        # Get all photos and videos
        print("\n" + "=" * 70)
        print("Querying all photos and videos...")
        print("=" * 70)

        nodes = ap.query("type:(PHOTOS OR VIDEOS)")
        total_items = len(nodes)

        print(f"\nFound {total_items:,} photos and videos!")

        if total_items == 0:
            print("No photos or videos found in your library.")
            return

        # Confirm download
        print("\n" + "=" * 70)
        print("Ready to download")
        print("=" * 70)

        download_path = input(f"\nEnter download path (default: ./downloads): ").strip() or "./downloads"

        confirm = input(f"\nDownload {total_items:,} items to '{download_path}'? (y/n): ").strip().lower()

        if confirm != 'y':
            print("Download cancelled.")
            return

        # Create download directory
        Path(download_path).mkdir(parents=True, exist_ok=True)

        # Download all media
        print("\n" + "=" * 70)
        print("Starting download...")
        print("=" * 70)
        print("\nThis may take a while depending on your library size.")
        print("Downloads will be saved with format: {node_id}_{filename}")

        ap.download(nodes.id, out=download_path)

        print("\n" + "=" * 70)
        print("Download Complete!")
        print("=" * 70)
        print(f"\nAll {total_items:,} items downloaded to: {Path(download_path).absolute()}")

    except KeyboardInterrupt:
        print("\n\nDownload interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure your cookies are correct and not expired")
        print("2. Try logging out and back into Amazon Photos")
        print("3. Get fresh cookies and try again")
        sys.exit(1)

if __name__ == '__main__':
    download_all_photos()
