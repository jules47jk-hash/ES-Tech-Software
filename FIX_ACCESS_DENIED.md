# Fix "Access Denied" Error on PythonAnywhere Updates

## Problem
You're getting "access denied" every time you try to run the update script on PythonAnywhere.

## Quick Fix (Try This First)

### Option 1: Run with Bash Explicitly (No Permissions Needed)
Instead of running `./update.sh`, use:

```bash
bash ~/embroidery_service_webapp/update.sh
```

This doesn't require execute permissions on the script.

---

## Complete Fix: Set Proper Permissions

### Step 1: Fix Script Permissions
Run these commands in PythonAnywhere Bash:

```bash
cd ~/embroidery_service_webapp
chmod +x update.sh
```

### Step 2: Fix Directory Permissions
Ensure your project directory has proper permissions:

```bash
chmod 755 ~/embroidery_service_webapp
```

### Step 3: Verify Permissions
Check that everything is set correctly:

```bash
ls -la ~/embroidery_service_webapp/update.sh
ls -ld ~/embroidery_service_webapp
```

The script should show `-rwxr-xr-x` (executable).
The directory should show `drwxr-xr-x` (readable/executable).

---

## Alternative: Manual Update (No Script Needed)

If the script still doesn't work, you can update manually:

### Step 1: Navigate to Project
```bash
cd ~/embroidery_service_webapp
```

### Step 2: Backup Database (Optional)
```bash
cp service.db service.db.backup.$(date +%Y%m%d_%H%M%S) 2>/dev/null || echo "No database to backup"
```

### Step 3: Pull Latest Changes
```bash
git fetch origin main
git pull origin main
```

If `git pull` fails, try:
```bash
git reset --hard origin/main
```

### Step 4: Restore Database (If Needed)
If your database was affected, restore from backup:
```bash
# List backups
ls -la service.db.backup.*

# Restore (replace TIMESTAMP with actual backup timestamp)
# cp service.db.backup.TIMESTAMP service.db
```

### Step 5: Update Dependencies
```bash
pip3.10 install --user -r requirements.txt
```

### Step 6: Reload Web App
1. Go to **"Web"** tab in PythonAnywhere dashboard
2. Click the big green **"Reload"** button

---

## Troubleshooting Specific Errors

### Error: "Permission denied: ./update.sh"
**Solution:** Run with `bash` explicitly:
```bash
bash ~/embroidery_service_webapp/update.sh
```

### Error: "Permission denied" when copying database
**Solution:** Check database file permissions:
```bash
cd ~/embroidery_service_webapp
ls -la service.db
chmod 666 service.db  # Make it writable
```

### Error: "Permission denied" during git operations
**Solution:** Check git directory permissions:
```bash
cd ~/embroidery_service_webapp
ls -la .git
chmod -R 755 .git
```

### Error: "Cannot write to directory"
**Solution:** Ensure you're in your home directory:
```bash
pwd  # Should show /home/jules47jk/embroidery_service_webapp
echo $HOME  # Should show /home/jules47jk
```

If you're not in your home directory, move the project:
```bash
cd ~
mv /path/to/wrong/location/embroidery_service_webapp ~/embroidery_service_webapp
```

---

## One-Line Update Command (No Script)

Copy and paste this entire command into PythonAnywhere Bash:

```bash
cd ~/embroidery_service_webapp && [ -f service.db ] && cp service.db service.db.backup.$(date +%Y%m%d_%H%M%S) 2>/dev/null || true && git fetch origin main && git pull origin main && pip3.10 install --user -r requirements.txt && echo "✅ Update complete! Now reload your web app."
```

---

## Verify Everything Works

After updating, verify:

1. **Check files updated:**
   ```bash
   cd ~/embroidery_service_webapp
   git log -1 --oneline
   ```

2. **Test app imports:**
   ```bash
   python3.10 -c "from app import app; print('✅ App imports OK')"
   ```

3. **Check database exists:**
   ```bash
   ls -la service.db
   ```

4. **Reload web app** in PythonAnywhere dashboard

---

## Still Not Working?

If you're still getting "access denied":

1. **Check the exact error message** - copy it here
2. **Check your PythonAnywhere username** - make sure paths use your actual username
3. **Try the manual update steps** above (no script needed)
4. **Check error log** in PythonAnywhere Web tab for more details

---

## Recommended Workflow (Going Forward)

**Always use this method to avoid permission issues:**

```bash
cd ~/embroidery_service_webapp
bash update.sh
```

Or use the manual steps above if the script continues to have issues.

