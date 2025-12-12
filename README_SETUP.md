# Embroidery Service Webapp - Setup Instructions

## Quick Start (For Testing)

### Option 1: Simple Python Setup (Recommended for Testing)

1. **Install Python** (if not already installed):
   - **See INSTALL_PYTHON.md for detailed step-by-step instructions**
   - Or download Python 3.8 or higher from https://www.python.org/downloads/
   - **IMPORTANT**: During installation, check "Add Python to PATH" (this is crucial!)

2. **Open Command Prompt or PowerShell** in the application folder

3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```
   python app.py
   ```

5. **Open your web browser** and go to:
   ```
   http://localhost:5000
   ```

The application will run on your local machine. Press `Ctrl+C` to stop it.

---

## Option 2: Create a Standalone Executable (For Non-Technical Users)

### Using PyInstaller:

1. **Install PyInstaller**:
   ```
   pip install pyinstaller
   ```

2. **Create the executable**:
   ```
   pyinstaller --onefile --add-data "templates;templates" --add-data "static;static" --name "EmbroideryService" app.py
   ```

3. **Distribute the entire `dist` folder** to your client

**Note**: The executable will be large (50-100MB) but includes everything needed.

---

## Option 3: Use the Included Batch Files

Two batch files are included:

### `start_app.bat` (Automatic)
- Checks for Python (tries multiple methods)
- Installs dependencies if needed
- Starts the application
- Opens the browser automatically
- **Just double-click to run**

### `RUN_APP.bat` (Manual/Alternative)
- Provides clearer error messages
- Step-by-step guidance
- Use this if `start_app.bat` doesn't work

**If you get "Python not found" error:**
- See `INSTALL_PYTHON.md` for detailed installation instructions
- Make sure Python is installed with "Add Python to PATH" checked

---

## Database

The application uses SQLite (included with Python). The database file `service.db` will be created automatically on first run.

**Important**: Make sure to backup `service.db` regularly as it contains all your data!

---

## Troubleshooting

### Port Already in Use
If you see "Address already in use", another instance is running. Close it or change the port in `app.py` (line 1397):
```python
app.run(debug=True, port=5001)  # Change 5001 to any available port
```

### Python Not Found
- Make sure Python is installed and added to PATH
- Try using `py` instead of `python` in commands
- Or use full path: `C:\Python39\python.exe app.py`

### Dependencies Not Installing
- Make sure you have internet connection
- Try: `pip install --upgrade pip` first
- Then: `pip install -r requirements.txt`

---

## For Production Deployment

For a production environment, consider:
- Using a proper web server (Gunicorn, Waitress)
- Setting up as a Windows Service
- Using a reverse proxy (nginx)
- Setting up SSL/HTTPS
- Regular database backups

---

## Support

If you encounter issues, check:
1. Python version (should be 3.8+)
2. All files are in the same folder
3. Firewall isn't blocking port 5000
4. No antivirus is blocking the application

