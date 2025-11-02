# Amazon Photos Download Guide

This guide will help you easily download **ALL** your photos and videos from Amazon Photos.

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Method 1: Simple Python Script (Recommended)](#method-1-simple-python-script-recommended)
- [Method 2: Web Interface](#method-2-web-interface)
- [Method 3: Using the Library Directly](#method-3-using-the-library-directly)
- [Getting Your Cookies](#getting-your-cookies)
- [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

The fastest way to download all your photos:

```bash
# Install the package
pip install -e .

# Run the download script
python download_all.py
```

Follow the prompts to enter your cookies and start downloading!

---

## Method 1: Simple Python Script (Recommended)

This is the **easiest** method for most users.

### Prerequisites

```bash
pip install -e .
```

### Usage

1. Run the script:
   ```bash
   python download_all.py
   ```

2. Follow the interactive prompts:
   - Select your region (US, Canada, Europe)
   - Enter your Amazon Photos cookies (see [Getting Your Cookies](#getting-your-cookies))
   - Confirm the download location
   - Wait for your photos to download!

### Features

- ✅ Downloads ALL photos and videos
- ✅ Interactive and user-friendly
- ✅ Shows progress during download
- ✅ Handles errors gracefully
- ✅ Works in all regions (US, Canada, Europe)

---

## Method 2: Web Interface

A browser-based interface with real-time progress updates.

### Prerequisites

```bash
pip install -e .
pip install flask flask-cors flask-socketio
```

### Usage

1. Start the web server:
   ```bash
   python server.py
   ```

2. Open your browser to: **http://localhost:5000**

3. Follow the on-screen instructions:
   - Enter your Amazon Photos cookies
   - Validate cookies
   - Click "Start Download"
   - Monitor progress in real-time!

### Features

- ✅ Beautiful web interface
- ✅ Real-time progress tracking
- ✅ Visual gallery of downloaded photos
- ✅ Pause/resume capability
- ✅ Works from any browser

---

## Method 3: Using the Library Directly

For advanced users who want full control.

### Example Code

```python
from amazon_photos import AmazonPhotos

# Initialize with your cookies
ap = AmazonPhotos(
    cookies={
        'session-id': 'YOUR_SESSION_ID',
        'ubid-main': 'YOUR_UBID_MAIN',      # For US
        'at-main': 'YOUR_AT_MAIN',          # For US
        # For Canada, use: ubid-acbca and at-acbca
        # For Europe, use: ubid-acb{tld} and at-acb{tld}
    },
    tmp='tmp',  # Optional: cache API responses
)

# Get all photos and videos
nodes = ap.query("type:(PHOTOS OR VIDEOS)")

print(f"Found {len(nodes):,} photos and videos!")

# Download all media
ap.download(nodes.id, out='my_photos')

print("Download complete!")
```

### Advanced Queries

You can filter what to download:

```python
# Only photos (no videos)
photos = ap.photos()

# Only videos
videos = ap.videos()

# Photos from a specific date
nodes = ap.query("type:(PHOTOS) AND timeYear:(2023) AND timeMonth:(12)")

# Photos with specific tags
nodes = ap.query("type:(PHOTOS) AND things:(beach OR sunset)")

# Photos from a specific location
nodes = ap.query("type:(PHOTOS) AND location:(USA#CA#Los Angeles)")
```

---

## 🍪 Getting Your Cookies

Amazon Photos requires authentication cookies. Here's how to get them:

### Step 1: Log in to Amazon Photos

1. Open your browser (Chrome, Firefox, Safari, etc.)
2. Go to Amazon Photos: https://www.amazon.com/photos
3. Log in to your account

### Step 2: Open Developer Tools

- **Chrome/Edge**: Press `F12` or `Ctrl+Shift+I` (Windows) / `Cmd+Option+I` (Mac)
- **Firefox**: Press `F12` or `Ctrl+Shift+I` (Windows) / `Cmd+Option+I` (Mac)
- **Safari**: Enable Developer menu first, then press `Cmd+Option+I`

### Step 3: Find Cookies

1. Click on the **Application** tab (Chrome) or **Storage** tab (Firefox)
2. In the left sidebar, expand **Cookies**
3. Click on `https://www.amazon.com` (or your country's domain)
4. Find and copy the following cookie values:

#### For United States (.com)
- `session-id`
- `ubid-main`
- `at-main`

#### For Canada (.ca)
- `session-id`
- `ubid-acbca`
- `at-acbca`

#### For Europe (e.g., .de, .uk, .fr)
- `session-id`
- `ubid-acb{tld}` (e.g., `ubid-acbde` for Germany)
- `at-acb{tld}` (e.g., `at-acbde` for Germany)

### Visual Guide

```
Developer Tools → Application/Storage → Cookies → amazon.com
├── session-id          → Copy this value
├── ubid-main           → Copy this value (US)
└── at-main             → Copy this value (US)
```

### Cookie Expiration

- Cookies typically expire after a few days
- If you get authentication errors, get fresh cookies
- You'll need to repeat this process periodically

---

## 🔧 Troubleshooting

### "BadAuthenticationData" Error

**Cause**: Your cookies have expired or are incorrect.

**Solution**:
1. Log out of Amazon Photos
2. Log back in
3. Get fresh cookies
4. Try again

### Download is Slow

**Cause**: Large library size or slow internet connection.

**Solution**:
- Be patient! Downloading thousands of photos takes time
- The download happens in parallel for faster speeds
- Consider using the batch method to download in chunks

### Script Crashes or Stops

**Cause**: Network issues or API rate limiting.

**Solution**:
- The script has automatic retry logic
- If it stops, just run it again
- Already downloaded photos won't be re-downloaded

### "No Photos Found"

**Cause**: Query filter is too restrictive or cookies are invalid.

**Solution**:
1. Verify your cookies are correct
2. Try the basic query: `ap.query("type:(PHOTOS OR VIDEOS)")`
3. Check if you actually have photos in your Amazon Photos account

### Import Error

**Cause**: Package not installed.

**Solution**:
```bash
pip install -e .
```

### Server Won't Start (Method 2)

**Cause**: Missing dependencies.

**Solution**:
```bash
pip install flask flask-cors flask-socketio
```

---

## 📊 Performance Tips

### Faster Downloads

1. **Use the async download method** (already built-in)
2. **Increase connection limits** (advanced):
   ```python
   from httpx import Limits

   ap = AmazonPhotos(
       cookies={...},
       limits=Limits(max_connections=4000)  # Default is 2000
   )
   ```

### Download in Batches

For very large libraries, download in batches:

```python
# Get all nodes
nodes = ap.query("type:(PHOTOS OR VIDEOS)")

# Download in batches of 1000
batch_size = 1000
for i in range(0, len(nodes), batch_size):
    batch = nodes.id[i:i+batch_size]
    ap.download(batch, out='downloads')
    print(f"Downloaded batch {i//batch_size + 1}")
```

---

## ❓ FAQ

**Q: Will this delete my photos from Amazon Photos?**
A: No! This only downloads copies. Your photos remain in Amazon Photos.

**Q: Can I download photos from a family vault?**
A: Yes, if you have access. Use the appropriate cookies and filters.

**Q: How long does it take?**
A: Depends on your library size. For reference:
- 1,000 photos: ~10-20 minutes
- 10,000 photos: ~1-2 hours
- 100,000 photos: ~10-15 hours

**Q: Can I resume a download?**
A: The current implementation downloads all items each time. To avoid re-downloads, move completed files to a different folder.

**Q: Does this work on Windows/Mac/Linux?**
A: Yes! Python is cross-platform.

**Q: Can I download specific albums?**
A: Yes, you can use the library's query filters to target specific albums or dates.

---

## 🆘 Getting Help

If you're still having trouble:

1. Check the logs in `log.log`
2. Make sure your cookies are fresh and valid
3. Verify you're using the correct cookie names for your region
4. Try the simple method first (Method 1)
5. Open an issue on GitHub with error details

---

## 🎉 Success!

Once your download completes, you'll have all your photos saved locally!

The files will be named in the format: `{node_id}_{original_filename}`

You can safely backup these files or organize them as needed.

**Happy downloading! 📸**
