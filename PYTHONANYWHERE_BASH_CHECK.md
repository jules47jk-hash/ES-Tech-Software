# PythonAnywhere Bash Verification Commands

## Check Your Setup via Bash

Run these commands in PythonAnywhere's Bash console to verify everything is correct:

### 1. Check Project Location
```bash
cd ~/embroidery_service_webapp
pwd
# Should show: /home/jules47jk/embroidery_service_webapp
```

### 2. Verify Files Exist
```bash
ls -la
# Should show: app.py, requirements.txt, templates/, etc.
```

### 3. Check WSGI File Content
```bash
cat /var/www/jules47jk_pythonanywhere_com_wsgi.py
```

**Expected content:**
```python
import sys
import os

path = '/home/jules47jk/embroidery_service_webapp'
if path not in sys.path:
    sys.path.insert(0, path)

os.chdir(path)

from app import app as application
```

### 4. Test Python Import
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
print("App imported successfully!")
print(f"App name: {app.name}")
exit()
```

### 5. Check Database File
```bash
cd ~/embroidery_service_webapp
ls -la service.db
# Should show the database file exists and has permissions
```

### 6. Test Database Connection
```bash
cd ~/embroidery_service_webapp
python3.10 -c "import sqlite3; conn = sqlite3.connect('service.db'); print('Database OK'); conn.close()"
```

---

## Fix WSGI File via Bash (if needed)

**Note:** PythonAnywhere manages the WSGI file, but you can check/edit it:

```bash
# View current WSGI file
cat /var/www/jules47jk_pythonanywhere_com_wsgi.py

# Edit WSGI file (if you have permissions)
nano /var/www/jules47jk_pythonanywhere_com_wsgi.py
```

**However**, it's better to edit it through the **"Web"** tab → **"WSGI configuration file"** link.

---

## Important: Working Directory Setting

**You CANNOT change the "Working directory" setting via Bash.**

This must be changed in the **"Web"** tab:
1. Click the pencil icon next to "Working directory"
2. Change to: `/home/jules47jk/embroidery_service_webapp`
3. Click Save

---

## After Making Changes

Always reload the web app:
- Go to **"Web"** tab → Click **"Reload"** button

