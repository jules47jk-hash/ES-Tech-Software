# How to Update Your App on PythonAnywhere

## Quick Update Process

### Step 1: Make Changes Locally
1. Edit files on your local computer (`C:\Users\Julian\embroidery_service_webapp\`)
2. Test locally if possible
3. Save your changes

### Step 2: Upload Changed Files
**Option A: Using Files Tab (Easiest for Single Files)**
1. Go to PythonAnywhere → **"Files"** tab
2. Navigate to `/home/jules47jk/embroidery_service_webapp/`
3. Click **"Upload a file"** button
4. Select the file(s) you changed from your local computer
5. Click **"Upload"** (it will ask to replace - click **"Yes"**)

**Option B: Using Bash (For Multiple Files or Git)**
1. Go to **"Consoles"** tab → **"Bash"**
2. If using Git:
   ```bash
   cd ~/embroidery_service_webapp
   git pull
   ```
3. Or manually copy/paste file contents:
   - Open file in Files tab
   - Delete old content
   - Paste new content
   - Save

### Step 3: Install New Dependencies (If Needed)
If you added new packages to `requirements.txt`:
```bash
cd ~/embroidery_service_webapp
pip3.10 install --user -r requirements.txt
```

### Step 4: Reload Web App
1. Go to **"Web"** tab
2. Click the big green **"Reload"** button
3. Wait 10-15 seconds for reload

### Step 5: Test Changes
Visit: `https://jules47jk.pythonanywhere.com`
- Test the changes you made
- Check error log if something doesn't work

---

## Common Update Scenarios

### Updating app.py
1. Edit `app.py` locally
2. Upload via **"Files"** tab → Replace existing `app.py`
3. **"Web"** tab → **"Reload"**

### Updating Templates (HTML files)
1. Edit files in `templates/` folder locally
2. Upload individual files or entire `templates/` folder
3. **"Web"** tab → **"Reload"**

### Updating Static Files (CSS, JS, images)
1. Edit files in `static/` folder locally
2. Upload files to `/home/jules47jk/embroidery_service_webapp/static/`
3. **"Web"** tab → **"Reload"**
4. **Clear browser cache** (Ctrl+F5) to see CSS/JS changes

### Adding New Python Packages
1. Add package to `requirements.txt` locally
2. Upload updated `requirements.txt`
3. Install:
   ```bash
   cd ~/embroidery_service_webapp
   pip3.10 install --user -r requirements.txt
   ```
4. **"Web"** tab → **"Reload"**

### Database Changes
**⚠️ IMPORTANT: Backup database first!**
1. Download `service.db` from **"Files"** tab (backup)
2. Make database changes locally if needed
3. Upload new `service.db` (or let app create it)
4. **"Web"** tab → **"Reload"**

---

## Using Git (Recommended for Larger Updates)

### Initial Setup (One-time)
1. Push your code to GitHub
2. In PythonAnywhere Bash:
   ```bash
   cd ~
   git clone https://github.com/jules47jk-hash/ES-Tech-Software.git embroidery_service_webapp
   ```

### Updating via Git
1. Push changes to GitHub/GitLab from local computer
2. In PythonAnywhere Bash:
   ```bash
   cd ~/embroidery_service_webapp
   git pull
   ```
3. Install any new dependencies:
   ```bash
   pip3.10 install --user -r requirements.txt
   ```
4. **"Web"** tab → **"Reload"**

---

## Best Practices

### Before Updating
- ✅ **Backup your database** (download `service.db`)
- ✅ Test changes locally if possible
- ✅ Note what files you're changing

### During Update
- ✅ Upload files one at a time or in small batches
- ✅ Check for errors after each upload
- ✅ Always reload after uploading

### After Updating
- ✅ Test the changes on the live site
- ✅ Check error log if something breaks
- ✅ Keep backups of working versions

---

## Troubleshooting Updates

### Changes Not Showing
1. **Clear browser cache** (Ctrl+F5 or Ctrl+Shift+R)
2. **Check file was uploaded** (verify file size/date in Files tab)
3. **Check error log** for import errors
4. **Reload web app** again

### Import Errors After Update
1. Check **"Error log"** for specific error
2. Verify syntax is correct (no typos)
3. Check all dependencies installed:
   ```bash
   pip3.10 list | grep -i flask
   ```

### Database Issues
1. **Restore from backup** if needed
2. Download `service.db` from Files tab
3. Upload previous working version

---

## Quick Reference

```bash
# Navigate to project
cd ~/embroidery_service_webapp

# Install/update dependencies
pip3.10 install --user -r requirements.txt

# Check if app imports correctly
python3.10 -c "from app import app; print('OK')"

# View error log (alternative to Web tab)
tail -n 50 ~/logs/jules47jk.pythonanywhere.com.error.log
```

---

## Summary Workflow

1. **Edit locally** → 2. **Upload files** → 3. **Install deps** (if needed) → 4. **Reload** → 5. **Test**

That's it! Your changes are live.

