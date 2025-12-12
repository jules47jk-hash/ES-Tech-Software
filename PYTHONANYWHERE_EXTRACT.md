# Extracting Files in PythonAnywhere Bash

## Extracting ZIP Files

### If you uploaded a ZIP file:

1. **Navigate to where you uploaded the ZIP:**
   ```bash
   cd ~
   # or
   cd ~/embroidery_service_webapp
   ```

2. **List files to see the ZIP:**
   ```bash
   ls -la
   ```

3. **Extract the ZIP file:**
   ```bash
   unzip your-file.zip
   ```

   **Example:**
   ```bash
   unzip embroidery_service_webapp.zip
   ```

4. **Extract to a specific folder:**
   ```bash
   unzip your-file.zip -d embroidery_service_webapp
   ```

5. **Extract without creating a folder (if ZIP contains files directly):**
   ```bash
   unzip -j your-file.zip -d embroidery_service_webapp
   ```

---

## Extracting Other Archive Types

### TAR.GZ files:
```bash
tar -xzf your-file.tar.gz
```

### TAR files:
```bash
tar -xf your-file.tar
```

### RAR files (if unrar is installed):
```bash
unrar x your-file.rar
```

---

## Step-by-Step Example

### Scenario: You uploaded `embroidery_service_webapp.zip`

1. **Open Bash console** (Consoles tab → Bash)

2. **Navigate to home directory:**
   ```bash
   cd ~
   ```

3. **List files to find your ZIP:**
   ```bash
   ls -la
   ```
   You should see `embroidery_service_webapp.zip`

4. **Extract it:**
   ```bash
   unzip embroidery_service_webapp.zip
   ```

5. **Check what was extracted:**
   ```bash
   ls -la
   ```

6. **If it created a folder, navigate into it:**
   ```bash
   cd embroidery_service_webapp
   ls -la
   ```

7. **Verify your files are there:**
   ```bash
   ls -la templates/
   ls -la static/
   ```

---

## If unzip is not available

If you get "command not found", install it:
```bash
sudo apt-get update
sudo apt-get install unzip
```

(Note: This might not work on free tier - use the Files tab instead)

---

## Alternative: Extract via Files Tab

If bash extraction doesn't work:

1. Go to **"Files"** tab
2. Navigate to your ZIP file
3. Click on the ZIP file
4. PythonAnywhere will show contents
5. You can download/extract individual files
6. Or use the **"Extract"** button if available

---

## Common Issues

### "unzip: command not found"
- Try using the Files tab interface instead
- Or upload files individually instead of ZIP

### Files extracted to wrong location
- Check where you are: `pwd`
- Move files: `mv extracted-folder/* ~/embroidery_service_webapp/`

### Permission denied
- Check permissions: `ls -la`
- Change permissions if needed: `chmod 755 filename`

---

## Quick Reference

```bash
# See current directory
pwd

# List files
ls -la

# Navigate
cd ~/embroidery_service_webapp

# Extract ZIP
unzip filename.zip

# Extract to specific folder
unzip filename.zip -d folder-name

# Remove ZIP after extraction (optional)
rm filename.zip
```

