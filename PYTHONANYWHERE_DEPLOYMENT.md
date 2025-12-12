# PythonAnywhere Deployment Guide

## Step-by-Step Deployment Instructions

### Step 1: Sign Up and Initial Setup

1. Go to **https://www.pythonanywhere.com/**
2. Sign up for a free account (or paid if needed)
3. Log in to your dashboard

---

### Step 2: Upload Your Files

**Option A: Using the Files Tab (Easiest)**

1. Click **"Files"** tab in the top menu
2. Navigate to `/home/yourusername/` (replace `yourusername` with your actual username)
3. Click **"Upload a file"** button
4. Upload all your files:
   - `app.py`
   - `import_parts_catalog.py`
   - `requirements.txt`
   - `templates/` folder (upload as zip, then extract)
   - `static/` folder (upload as zip, then extract)

**Option B: Using Git (Recommended)**

1. Push your code to GitHub
2. Open **"Consoles"** tab → **"Bash"**
3. Run:
   ```bash
   cd ~
   git clone https://github.com/jules47jk-hash/ES-Tech-Software.git embroidery_service_webapp
   cd embroidery_service_webapp
   ```

---

### Step 3: Install Dependencies

1. Go to **"Consoles"** tab → Click **"Bash"**
2. Navigate to your project folder:
   ```bash
   cd ~/embroidery_service_webapp
   # or wherever your files are
   ```
3. Install packages:
   ```bash
   pip3.10 install --user -r requirements.txt
   ```
   (Use `pip3.10` or `pip3.11` depending on your Python version)

---

### Step 4: Configure the Web App

1. Click **"Web"** tab in the top menu
2. Click **"Add a new web app"**
3. Choose **"Flask"**
4. Select **Python 3.10** (or 3.11)
5. Click **"Next"**
6. In the **"Path"** field, enter: `/home/yourusername/embroidery_service_webapp/app.py`
   - Replace `yourusername` with your actual username
   - Adjust path if your folder has a different name
7. Click **"Next"** → **"Finish"**

---

### Step 5: Configure WSGI File

1. In the **"Web"** tab, find **"WSGI configuration file"** link
2. Click it to edit
3. **Delete all the default content** and replace with:

```python
import sys
import os

# Add your project directory to the path
path = '/home/yourusername/embroidery_service_webapp'
if path not in sys.path:
    sys.path.insert(0, path)

# Change to your project directory
os.chdir(path)

# Import your Flask app
# Note: init_db() is already called automatically in app.py when the module loads
from app import app as application

if __name__ == "__main__":
    application.run()
```

**Important:** Replace `yourusername` with your actual PythonAnywhere username!

---

### Step 6: Configure Static Files

1. In the **"Web"** tab, scroll down to **"Static files"**
2. Click **"Add a new static files mapping"**
3. **URL:** `/static/`
4. **Directory:** `/home/yourusername/embroidery_service_webapp/static/`
5. Click the **"+"** button

---

### Step 7: Update Database Path (If Needed)

PythonAnywhere uses a different file system. Check if your `app.py` uses absolute paths correctly. The current code should work, but verify the database is created in the right location.

You can test by opening a Bash console and checking:
```bash
cd ~/embroidery_service_webapp
ls -la service.db
```

---

### Step 8: Reload Web App

1. Go back to **"Web"** tab
2. Click the big green **"Reload"** button
3. Your app should now be live!

---

### Step 9: Access Your App

Your app will be available at:
- **Free tier:** `https://yourusername.pythonanywhere.com`
- **Paid tier:** Your custom domain (if configured)

---

## Troubleshooting

### "Module not found" errors
- Make sure you installed packages: `pip3.10 install --user -r requirements.txt`
- Check Python version matches (3.10 vs 3.11)
- Try: `pip3.10 install --user flask flask-login`

### Database not working
- Check file permissions: `chmod 666 service.db` (if needed)
- Verify database path in `app.py` is correct
- Check error logs in **"Web"** tab → **"Error log"**

### Static files not loading
- Verify static files mapping in **"Web"** tab
- Check file paths are correct
- Make sure `static/` folder was uploaded correctly

### Login not working
- Check Flask-Login is installed: `pip3.10 install --user flask-login`
- Verify `app.secret_key` is set (required for sessions)
- Check error logs for specific errors

### 500 Internal Server Error
1. Go to **"Web"** tab → **"Error log"**
2. Read the error message
3. Common issues:
   - Missing packages
   - Wrong file paths
   - Syntax errors in code

---

## Important Notes for PythonAnywhere

### Free Tier Limitations:
- ✅ 1 web app
- ✅ 512 MB disk space
- ✅ Can be accessed from anywhere
- ❌ Sleeps after 3 months of inactivity (wakes on next visit)
- ❌ Limited CPU time

### Paid Tier Benefits:
- No sleeping
- More disk space
- Custom domains
- More CPU time

### File Paths:
- Your home directory: `/home/yourusername/`
- Always use absolute paths or paths relative to your project folder
- Database will be created in your project folder

### Reloading:
- After any code changes, click **"Reload"** in the **"Web"** tab
- Changes take effect immediately after reload

---

## Quick Commands Reference

```bash
# Navigate to project
cd ~/embroidery_service_webapp

# Install packages
pip3.10 install --user -r requirements.txt

# Check if files exist
ls -la

# View error logs (in Web tab)
# Or in console:
tail -n 50 ~/logs/yourusername.pythonanywhere.com.error.log

# Test database
python3.10
>>> import sqlite3
>>> conn = sqlite3.connect('service.db')
>>> conn.close()
```

---

## Updating Your App

1. Upload new files (or `git pull` if using Git)
2. Install any new packages: `pip3.10 install --user new-package`
3. Go to **"Web"** tab → Click **"Reload"**

---

## Database Backup

To backup your database:
1. Go to **"Files"** tab
2. Navigate to your project folder
3. Download `service.db` file
4. Keep backups regularly!

---

## Security Reminder

Before deploying:
- ✅ Change `app.secret_key` to a strong random string
- ✅ Set `debug=False` in production (already done if using WSGI)
- ✅ Your login credentials are: Fairfield / ES2025

---

## Support

If you encounter issues:
1. Check **"Web"** tab → **"Error log"**
2. Check **"Tasks"** tab for scheduled tasks
3. PythonAnywhere has helpful documentation and forums

