# Database Protection Guide

## How Database Protection Works

Your database (`service.db`) is **automatically protected** from being overwritten during updates.

### Protection Mechanisms

1. **`.gitignore` File**
   - Database files (`*.db`, `service.db*`) are listed in `.gitignore`
   - This means Git will **never** track or commit your database
   - Your database will **never** be pushed to GitHub

2. **Update Script Protection**
   - The `update.sh` script explicitly backs up and restores the database
   - Even if something goes wrong, your database is safe

3. **Separate Databases**
   - Your local computer has its own `service.db`
   - PythonAnywhere has its own `service.db`
   - They are completely separate and independent

---

## What This Means

✅ **Safe to push updates** - Your database won't be affected  
✅ **Web data is preserved** - All entries made on the live site are saved  
✅ **Local data stays local** - Your local database won't affect the web version  
✅ **No data loss** - Updates won't overwrite existing data  

---

## Database Locations

- **Local Computer:** `C:\Users\Julian\embroidery_service_webapp\service.db`
- **PythonAnywhere:** `/home/jules47jk/embroidery_service_webapp/service.db`

These are **separate files** and don't sync with each other.

---

## Manual Database Backup (Optional)

If you want to backup your database before updates:

### On PythonAnywhere:
```bash
cd ~/embroidery_service_webapp
cp service.db service.db.backup.$(date +%Y%m%d)
```

### Download Backup:
1. Go to **"Files"** tab
2. Navigate to your project folder
3. Download `service.db` to your computer

---

## Restoring Database

If you ever need to restore a backup:

```bash
cd ~/embroidery_service_webapp
cp service.db.backup.YYYYMMDD service.db
```

Then reload the web app.

---

## Important Notes

- ⚠️ **Never commit `service.db`** - It's in `.gitignore` for a reason
- ⚠️ **Never push database files** - They contain sensitive data
- ✅ **Updates are safe** - Code updates won't affect your database
- ✅ **Data is preserved** - All web entries are saved permanently

---

## Troubleshooting

### "Database is empty after update"
- Check if `service.db` exists: `ls -la service.db`
- Check file permissions: `chmod 666 service.db`
- Restore from backup if needed

### "Want to sync database between local and web"
- This is **not recommended** - they should stay separate
- If needed, manually download from PythonAnywhere and replace local file
- Or upload local file to PythonAnywhere (will overwrite web data)

---

## Summary

Your database is **fully protected**. When you push code updates:
- ✅ Code files update
- ✅ Templates update  
- ✅ Dependencies update
- ❌ Database does NOT update (preserved)

Your web data is safe! 🎉

