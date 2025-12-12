# Fixing "Hello from Flask!" Issue on PythonAnywhere

## Problem
You're seeing "Hello from Flask!" instead of your actual app, and you can't edit the working directory setting.

## Solution: Fix the WSGI File

Since you can't edit the working directory, we need to make sure the WSGI file explicitly sets it.

### Step 1: Open WSGI Configuration File

1. Go to **"Web"** tab
2. Click the link: **"WSGI configuration file"** (`/var/www/jules47jk_pythonanywhere_com_wsgi.py`)

### Step 2: Replace ALL Content

**Delete everything** in the WSGI file and replace with this exact content:

```python
import sys
import os

# Get the directory where this WSGI file is located
# Then set the project path explicitly
project_path = '/home/jules47jk/embroidery_service_webapp'

# Add to Python path
if project_path not in sys.path:
    sys.path.insert(0, project_path)

# CRITICAL: Change working directory to project folder
os.chdir(project_path)

# Import the Flask app
from app import app as application

# This is required for PythonAnywhere
if __name__ == "__main__":
    application.run()
```

### Step 3: Save and Reload

1. Click **"Save"** button
2. Go back to **"Web"** tab
3. Click the big green **"Reload"** button

---

## Alternative: Check What's Actually Running

If the above doesn't work, the WSGI file might be importing a default Flask app.

### Check Current WSGI File Content

In Bash console, run:
```bash
cat /var/www/jules47jk_pythonanywhere_com_wsgi.py
```

Look for:
- ❌ `from flask import Flask` (this creates a default app)
- ❌ `app = Flask(__name__)` (this creates a default app)
- ✅ `from app import app` (this imports YOUR app)

If you see the ❌ items, that's the problem - replace with the ✅ version above.

---

## Verify Your App Files Are Correct

In Bash:
```bash
cd ~/embroidery_service_webapp
ls -la app.py
cat app.py | head -20
```

Make sure `app.py` exists and has your Flask app defined.

---

## Test Import in Bash

```bash
cd ~/embroidery_service_webapp
python3.10
```

Then in Python:
```python
import sys
sys.path.insert(0, '/home/jules47jk/embroidery_service_webapp')
import os
os.chdir('/home/jules47jk/embroidery_service_webapp')
from app import app
print(f"App routes: {[r.rule for r in app.url_map.iter_rules()]}")
exit()
```

This should show your routes like `/`, `/jobs`, `/login`, etc.

---

## Common Issues

### Issue 1: WSGI file has default Flask app
**Fix:** Replace with the WSGI content above that imports YOUR app.

### Issue 2: Wrong path in WSGI file
**Fix:** Make sure `project_path = '/home/jules47jk/embroidery_service_webapp'` matches your actual folder name.

### Issue 3: App not in correct location
**Fix:** Make sure `app.py` is in `/home/jules47jk/embroidery_service_webapp/`

---

## After Fixing

1. Save WSGI file
2. Reload web app
3. Visit: `https://jules47jk.pythonanywhere.com`
4. You should see the **login page**, not "Hello from Flask!"

