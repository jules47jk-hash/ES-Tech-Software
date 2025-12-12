# Distribution Guide for Clients

## What to Send to Your Client

### Option A: Source Code Package (Easiest for Testing)

**Send these files/folders:**
- `app.py` (main application)
- `import_parts_catalog.py` (optional utility)
- `requirements.txt` (dependencies list)
- `start_app.bat` (easy launcher for Windows)
- `README_SETUP.md` (setup instructions)
- `templates/` folder (all HTML templates)
- `static/` folder (CSS, images, etc.)
- `service.db` (if you want to include sample data, otherwise it will be created empty)

**Do NOT send:**
- `__pycache__/` folder (can be regenerated)
- `.db.backup` files (unless needed)

**Instructions for client:**
1. Extract all files to a folder (e.g., `C:\EmbroideryService\`)
2. Double-click `start_app.bat`
3. Browser will open automatically at http://localhost:5000

---

### Option B: Standalone Executable (For Non-Technical Users)

**Steps to create:**

1. Install PyInstaller on your machine:
   ```
   pip install pyinstaller
   ```

2. Create the executable:
   ```
   pyinstaller --onefile --windowed --add-data "templates;templates" --add-data "static;static" --name "EmbroideryService" --icon=static/logo.png app.py
   ```

3. **Send to client:**
   - The `.exe` file from `dist/` folder
   - The `templates/` folder
   - The `static/` folder
   - Instructions to keep all files in the same folder

**Note**: The executable will be large (~50-100MB) but includes Python and all dependencies.

---

### Option C: ZIP Package with Instructions

**Create a ZIP file containing:**
```
EmbroideryService/
├── app.py
├── import_parts_catalog.py
├── requirements.txt
├── start_app.bat
├── README_SETUP.md
├── templates/
├── static/
└── (optional: empty service.db for fresh start)
```

**Send the ZIP file** and ask client to:
1. Extract to a folder
2. Follow README_SETUP.md instructions
3. Or simply double-click `start_app.bat`

---

## Pre-Distribution Checklist

- [ ] Test the application on a clean Windows machine
- [ ] Remove any test/sample data from `service.db` (or provide empty database)
- [ ] Update `app.secret_key` in `app.py` for production (line 8)
- [ ] Consider changing `debug=True` to `debug=False` in `app.py` (line 1397)
- [ ] Verify all static files (logo.png, etc.) are included
- [ ] Test the `start_app.bat` file works
- [ ] Create a backup of your own `service.db` before sending

---

## Security Notes

**Before distributing:**
1. Change the secret key in `app.py`:
   ```python
   app.secret_key = "your-unique-secret-key-here"
   ```

2. For production, disable debug mode:
   ```python
   app.run(debug=False, host='127.0.0.1', port=5000)
   ```

3. Consider adding authentication if the app will be accessible over a network

---

## Network Access (Optional)

If you want the client to access the app from other devices on their network:

Change in `app.py` (line 1397):
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

Then access from other devices using: `http://[client-pc-ip]:5000`

**Warning**: Only do this on a trusted network and consider adding authentication!

---

## Support for Client

Provide these troubleshooting steps:

1. **Application won't start:**
   - Check Python is installed: `python --version`
   - Check dependencies: `pip install -r requirements.txt`
   - Check firewall isn't blocking port 5000

2. **Database issues:**
   - Make sure `service.db` file exists and isn't read-only
   - Check folder has write permissions

3. **Port already in use:**
   - Close other instances of the app
   - Or change port in `app.py`

---

## Alternative: Cloud Deployment

For easier access, consider deploying to:
- **Heroku** (free tier available)
- **PythonAnywhere** (free tier available)
- **DigitalOcean** (paid, but reliable)
- **AWS/Azure** (for enterprise)

This allows client to access via web browser without installing anything locally.

