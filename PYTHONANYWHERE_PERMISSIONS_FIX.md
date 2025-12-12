# Fixing Permission Denied Error on PythonAnywhere

## Problem
You're getting: **"Permission denied: You do not have write permissions for directory"**

This happens when the app tries to create/write files in a directory where you don't have write access.

---

## Solution 1: Verify Your Project Location

**Make sure your project is in your home directory:**

1. Open **"Consoles"** tab → **"Bash"**
2. Check where you are:
   ```bash
   pwd
   ```
   Should show: `/home/yourusername/`

3. List your files:
   ```bash
   ls -la
   ```

4. If your project folder is NOT in `/home/yourusername/`, move it there:
   ```bash
   cd ~
   # If your project is elsewhere, move it:
   mv /path/to/old/location/embroidery_service_webapp ~/embroidery_service_webapp
   ```

---

## Solution 2: Fix Directory Permissions

**Ensure your project directory has write permissions:**

1. Open **"Consoles"** tab → **"Bash"**
2. Navigate to your project:
   ```bash
   cd ~/embroidery_service_webapp
   ```

3. Check current permissions:
   ```bash
   ls -la
   ```

4. Fix permissions (if needed):
   ```bash
   chmod 755 ~/embroidery_service_webapp
   chmod 666 ~/embroidery_service_webapp/service.db 2>/dev/null || echo "Database doesn't exist yet, will be created"
   ```

---

## Solution 3: Create Database Manually First

**Create the database file before running the app:**

1. Open **"Consoles"** tab → **"Bash"**
2. Navigate to your project:
   ```bash
   cd ~/embroidery_service_webapp
   ```

3. Create an empty database file:
   ```bash
   touch service.db
   chmod 666 service.db
   ```

4. Or initialize it with Python:
   ```bash
   python3.10
   ```
   Then in Python:
   ```python
   import sqlite3
   conn = sqlite3.connect('service.db')
   conn.close()
   exit()
   ```

5. Set permissions:
   ```bash
   chmod 666 service.db
   ```

---

## Solution 4: Update WSGI Configuration

**Make sure your WSGI file sets the correct working directory:**

1. Go to **"Web"** tab
2. Click **"WSGI configuration file"**
3. Ensure it contains:
   ```python
   import sys
   import os
   
   # IMPORTANT: Replace 'yourusername' with your actual username!
   path = '/home/yourusername/embroidery_service_webapp'
   if path not in sys.path:
       sys.path.insert(0, path)
   
   # Change to your project directory (THIS IS CRITICAL!)
   os.chdir(path)
   
   # Import your Flask app
   from app import app as application
   
   # Initialize database on startup
   from app import init_db
   init_db()
   ```

**Key point:** The `os.chdir(path)` line ensures the app runs from your project directory, so `service.db` will be created there.

---

## Solution 5: Check Error Logs

**Find the exact error:**

1. Go to **"Web"** tab
2. Click **"Error log"** link
3. Look for the exact directory path mentioned in the error
4. The error will tell you which directory doesn't have write permissions

---

## Solution 6: Verify File Structure

**Make sure your files are in the right place:**

1. Open **"Files"** tab
2. Navigate to `/home/yourusername/embroidery_service_webapp/`
3. You should see:
   - `app.py`
   - `requirements.txt`
   - `templates/` folder
   - `static/` folder (if you have one)
   - `service.db` (will be created automatically)

---

## Quick Diagnostic Commands

Run these in Bash to diagnose:

```bash
# 1. Check current directory
pwd

# 2. Check if you're in home directory
echo $HOME

# 3. Check project exists
ls -la ~/embroidery_service_webapp

# 4. Check permissions
ls -ld ~/embroidery_service_webapp

# 5. Test write access
touch ~/embroidery_service_webapp/test_write.txt
rm ~/embroidery_service_webapp/test_write.txt
echo "Write access OK!"

# 6. Check database location
cd ~/embroidery_service_webapp
python3.10 -c "import os; print(os.path.abspath('service.db'))"
```

---

## Most Common Fix

**99% of the time, this fixes it:**

1. Open **"Consoles"** → **"Bash"**
2. Run:
   ```bash
   cd ~/embroidery_service_webapp
   chmod 755 .
   touch service.db
   chmod 666 service.db
   ```

3. Go to **"Web"** tab → Click **"Reload"**

---

## Still Not Working?

If none of the above works:

1. **Check the exact error message** in **"Web"** tab → **"Error log"**
2. The error will show the exact directory path that's causing issues
3. Make sure that directory is:
   - Inside `/home/yourusername/`
   - Has write permissions (`chmod 755` for directories, `chmod 666` for files)

---

## Important Notes

- **Never** try to write to `/var/`, `/usr/`, `/etc/`, or other system directories
- **Always** keep your project in `/home/yourusername/`
- PythonAnywhere free tier has limited write access - only in your home directory
- Database file must be in a directory you own (your home directory)

---

## After Fixing

Once permissions are fixed:

1. Go to **"Web"** tab
2. Click **"Reload"** button
3. Visit your site: `https://yourusername.pythonanywhere.com`
4. You should see the login page!

