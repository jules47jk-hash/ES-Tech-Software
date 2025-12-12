# PythonAnywhere Debugging Steps

## Step 1: Check WSGI File Content

Run this in Bash:
```bash
cat /var/www/jules47jk_pythonanywhere_com_wsgi.py
```

**What to look for:**
- Should have: `from app import app as application`
- Should NOT have: `from flask import Flask` or `app = Flask(__name__)`

---

## Step 2: Check Error Logs

1. Go to **"Web"** tab
2. Click **"Error log"** link
3. Copy the latest error messages and share them

---

## Step 3: Verify Your App Files

In Bash:
```bash
cd ~/embroidery_service_webapp
ls -la
```

Should show:
- `app.py`
- `templates/` folder
- `requirements.txt`

---

## Step 4: Test App Import

In Bash:
```bash
cd ~/embroidery_service_webapp
python3.10 -c "from app import app; print('SUCCESS')"
```

If this fails, there's an error in your app.py file.

---

## Step 5: Check What Routes Are Registered

In Bash:
```bash
cd ~/embroidery_service_webapp
python3.10 << EOF
import sys
sys.path.insert(0, '/home/jules47jk/embroidery_service_webapp')
import os
os.chdir('/home/jules47jk/embroidery_service_webapp')
from app import app
print("Routes:")
for rule in app.url_map.iter_rules():
    print(f"  {rule.rule} -> {rule.endpoint}")
EOF
```

This should show routes like `/`, `/login`, `/jobs`, etc.

---

## Common Issues & Fixes

### Issue: "Hello from Flask!" still showing
**Cause:** WSGI file is importing a default Flask app
**Fix:** Make sure WSGI file has `from app import app as application` (not `from flask import Flask`)

### Issue: ImportError or ModuleNotFoundError
**Cause:** Missing packages or wrong Python version
**Fix:** 
```bash
cd ~/embroidery_service_webapp
pip3.10 install --user -r requirements.txt
```

### Issue: 500 Internal Server Error
**Cause:** Error in app.py or missing database
**Fix:** Check error log, create database:
```bash
cd ~/embroidery_service_webapp
touch service.db
chmod 666 service.db
```

### Issue: Can't find templates
**Cause:** Wrong working directory
**Fix:** Make sure WSGI file has `os.chdir('/home/jules47jk/embroidery_service_webapp')`

---

## Quick Fix Checklist

- [ ] WSGI file imports YOUR app: `from app import app as application`
- [ ] WSGI file sets working directory: `os.chdir('/home/jules47jk/embroidery_service_webapp')`
- [ ] All packages installed: `pip3.10 install --user -r requirements.txt`
- [ ] Database file exists: `ls -la service.db`
- [ ] Reloaded web app after changes
- [ ] Checked error log for specific errors

