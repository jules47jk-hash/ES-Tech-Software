# Python Installation Guide for Clients

## Quick Installation Steps

### Step 1: Download Python
1. Go to: **https://www.python.org/downloads/**
2. Click the big yellow "Download Python" button
3. The download will start automatically

### Step 2: Install Python
1. **Run the downloaded installer** (python-3.x.x.exe)
2. **IMPORTANT**: Check the box that says **"Add Python to PATH"** at the bottom
   - This is crucial! Without this, the application won't work.
3. Click **"Install Now"**
4. Wait for installation to complete
5. Click **"Close"** when done

### Step 3: Verify Installation
1. Press `Windows Key + R`
2. Type: `cmd` and press Enter
3. In the command window, type: `python --version`
4. You should see something like: `Python 3.11.5`
5. If you see an error, try: `py --version`

### Step 4: Run the Application
1. Go back to the application folder
2. Double-click `start_app.bat`
3. The application should start!

---

## Troubleshooting

### "Python is not recognized"
**Solution**: Python wasn't added to PATH during installation.

**Option A - Reinstall Python:**
1. Uninstall Python from Control Panel
2. Download and install again
3. **Make sure to check "Add Python to PATH"**

**Option B - Add Python to PATH manually:**
1. Find where Python is installed (usually `C:\Users\YourName\AppData\Local\Programs\Python\Python3xx\`)
2. Press `Windows Key`, type "Environment Variables"
3. Click "Edit the system environment variables"
4. Click "Environment Variables" button
5. Under "System variables", find "Path" and click "Edit"
6. Click "New" and add: `C:\Users\YourName\AppData\Local\Programs\Python\Python3xx\`
7. Click "New" again and add: `C:\Users\YourName\AppData\Local\Programs\Python\Python3xx\Scripts\`
8. Click OK on all windows
9. **Restart your computer**
10. Try running `start_app.bat` again

### "pip is not recognized"
**Solution**: Use `python -m pip` instead, or reinstall Python with PATH option checked.

### Still Having Issues?
Try running the application manually:
1. Open Command Prompt in the application folder
2. Type: `py app.py` (or `python app.py`)
3. If that works, the batch file needs fixing - contact support

---

## Alternative: Use Python Launcher
If `python` doesn't work, try `py`:
- In Command Prompt, type: `py app.py`
- This uses the Windows Python Launcher

---

## Need Help?
Contact support with:
- Your Windows version (Windows 10/11)
- The exact error message you see
- Whether Python appears in "Add or Remove Programs"

