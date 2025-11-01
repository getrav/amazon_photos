# Quick Start Guide - Download Your Amazon Photos

## 🚀 Fastest Way to Download All Your Photos

### Step 1: Install the Package

```bash
pip install -e .
```

### Step 2: Run the Download Script

```bash
python download_all.py
```

### Step 3: Follow the Prompts

1. Select your region (US/Canada/Europe)
2. Enter your Amazon Photos cookies (see below)
3. Confirm download location
4. Wait for download to complete!

---

## 🍪 How to Get Your Cookies (2 minutes)

1. **Open Amazon Photos** in your browser
   - Go to https://www.amazon.com/photos and log in

2. **Open Developer Tools**
   - Press `F12` (or `Ctrl+Shift+I` on Windows, `Cmd+Option+I` on Mac)

3. **Find Cookies**
   - Click the **Application** tab (Chrome) or **Storage** tab (Firefox)
   - Expand **Cookies** in the left sidebar
   - Click on your Amazon domain (e.g., `https://www.amazon.com`)

4. **Copy These Values:**

   **For United States:**
   - `session-id`
   - `ubid-main`
   - `at-main`

   **For Canada:**
   - `session-id`
   - `ubid-acbca`
   - `at-acbca`

   **For Europe (e.g., Germany, UK, France):**
   - `session-id`
   - `ubid-acb{tld}` (replace {tld} with your country code)
   - `at-acb{tld}` (replace {tld} with your country code)

5. **Paste into the script** when prompted!

---

## 🌐 Alternative: Use the Web Interface

Prefer a browser interface with real-time progress?

```bash
# Install web dependencies
pip install -r requirements-web.txt

# Start the server
python server.py

# Open browser to http://localhost:5000
```

---

## ✅ That's It!

Your photos will download to the `./downloads` folder (or wherever you specify).

Files are named: `{node_id}_{original_filename}`

---

## 📚 Need More Help?

See the full [DOWNLOAD_GUIDE.md](DOWNLOAD_GUIDE.md) for:
- Detailed troubleshooting
- Advanced usage
- Performance tips
- FAQ

---

## 💡 Pro Tips

- **Cookies expire**: If you get errors, get fresh cookies
- **Large libraries**: Be patient, downloads take time
- **Already installed?**: Just run `python download_all.py`
- **Want to filter?**: See DOWNLOAD_GUIDE.md for advanced queries

**Happy downloading! 📸**
