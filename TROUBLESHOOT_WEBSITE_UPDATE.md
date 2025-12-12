# Troubleshooting Website Not Updating

## Step 1: Verify Files Were Actually Updated

Check if the files changed on PythonAnywhere:

```bash
cd ~/embroidery_service_webapp

# Check current commit
git log -1 --oneline

# Verify app.py doesn't have login references
grep -i "login_required\|@login" app.py
# Should return nothing

# Check if login route exists
grep -i "def login\|/login" app.py
# Should return nothing

# Check base.html doesn't have logout link
grep -i "logout" templates/base.html
# Should return nothing
```

---

## Step 2: Check Error Logs

**This is the most important step!**

1. Go to **"Web"** tab in PythonAnywhere
2. Click **"Error log"** link
3. Look for any errors (especially import errors or syntax errors)
4. Copy any error messages

Common errors:
- `ModuleNotFoundError: No module named 'flask_login'` - Flask-Login still installed
- `NameError: name 'login_required' is not defined` - Old code still running
- Syntax errors

---

## Step 3: Verify Dependencies

Make sure Flask-Login is NOT installed (since we removed it):

```bash
pip3.10 list | grep -i flask
```

If Flask-Login is still installed, uninstall it:
```bash
pip3.10 uninstall Flask-Login -y
```

---

## Step 4: Force Reload

1. Go to **"Web"** tab
2. Click **"Reload"** button
3. Wait 15-20 seconds (not just 10)
4. Check if the reload was successful (should show green checkmark)

---

## Step 5: Clear Browser Cache

**Very important!** Your browser might be caching the old version:

- **Chrome/Edge:** Press `Ctrl+Shift+Delete` → Clear cached images and files → Clear data
- **Or:** Press `Ctrl+F5` (hard refresh)
- **Or:** Use incognito/private window
- **Or:** Clear browser cache completely

---

## Step 6: Verify WSGI File

Check if WSGI file is correct:

```bash
cat /var/www/jules47jk_pythonanywhere_com_wsgi.py
```

Should import `app` correctly. If it has old code, it might be cached.

---

## Step 7: Check File Permissions

```bash
cd ~/embroidery_service_webapp
ls -la app.py templates/base.html
```

Files should be readable (not permission denied).

---

## Step 8: Test Import

Test if app.py can be imported without errors:

```bash
cd ~/embroidery_service_webapp
python3.10 -c "from app import app; print('SUCCESS')"
```

If this fails, there's an error in app.py.

---

## Step 9: Check What's Actually Running

Visit your site and check:
- Does it still show login page? (old version)
- Does it go straight to jobs? (new version)
- Any error messages?

---

## Quick Diagnostic Script

Run this all at once:

```bash
cd ~/embroidery_service_webapp && \
echo "=== Commit ===" && \
git log -1 --oneline && \
echo "" && \
echo "=== Login Check ===" && \
grep -c "login_required\|def login" app.py && \
echo "" && \
echo "=== Import Test ===" && \
python3.10 -c "from app import app; print('Import OK')" && \
echo "" && \
echo "=== Flask-Login Check ===" && \
pip3.10 list | grep -i flask-login || echo "Flask-Login not installed (good)"
```

---

## Most Common Issues

### Issue 1: Browser Cache
**Fix:** Clear cache completely or use incognito mode

### Issue 2: Error in app.py
**Fix:** Check error log, fix syntax errors

### Issue 3: Flask-Login Still Installed
**Fix:** `pip3.10 uninstall Flask-Login -y` then reload

### Issue 4: Old Code Cached
**Fix:** Reload web app multiple times, wait longer

### Issue 5: Wrong Files Pulled
**Fix:** `git reset --hard origin/main` to force match GitHub

---

## Nuclear Option: Complete Reset

If nothing works:

```bash
cd ~/embroidery_service_webapp
git fetch origin
git reset --hard origin/main
pip3.10 uninstall Flask-Login -y
pip3.10 install --user -r requirements.txt
```

Then reload web app and clear browser cache.

