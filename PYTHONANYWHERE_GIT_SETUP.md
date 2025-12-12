# PythonAnywhere Git Setup

## Option 1: Connect Existing Folder to GitHub (Recommended)

Since your app is already working, we'll connect the existing folder:

### Step 1: Open Bash Console
1. Go to PythonAnywhere → **"Consoles"** tab
2. Click **"Bash"**

### Step 2: Navigate to Your Project
```bash
cd ~/embroidery_service_webapp
```

### Step 3: Initialize Git (if not already done)
```bash
git init
```

### Step 4: Add GitHub Remote
```bash
git remote add origin https://github.com/jules47jk-hash/ES-Tech-Software.git
```

### Step 5: Check Current Status
```bash
git status
```

### Step 6: Add All Files
```bash
git add .
```

### Step 7: Commit Local Files
```bash
git commit -m "Initial PythonAnywhere setup"
```

### Step 8: Connect to GitHub
```bash
git branch -M main
git pull origin main --allow-unrelated-histories
```

If there are conflicts, you can force it (be careful - this overwrites local with GitHub):
```bash
git fetch origin
git reset --hard origin/main
```

---

## Option 2: Fresh Clone (If Option 1 Doesn't Work)

**⚠️ Warning:** This will replace your current files!

### Step 1: Backup Current Files
```bash
cd ~
cp -r embroidery_service_webapp embroidery_service_webapp_backup
```

### Step 2: Remove Old Folder
```bash
rm -rf embroidery_service_webapp
```

### Step 3: Clone from GitHub
```bash
git clone https://github.com/jules47jk-hash/ES-Tech-Software.git embroidery_service_webapp
```

### Step 4: Restore Database (if needed)
```bash
cp embroidery_service_webapp_backup/service.db embroidery_service_webapp/
```

### Step 5: Install Dependencies
```bash
cd ~/embroidery_service_webapp
pip3.10 install --user -r requirements.txt
```

### Step 6: Reload Web App
- Go to **"Web"** tab → Click **"Reload"**

---

## After Setup: Update Workflow

### From Your Computer (After Making Changes):
```powershell
cd C:\Users\Julian\embroidery_service_webapp
git add .
git commit -m "Description of changes"
git push
```

### On PythonAnywhere (To Get Updates):
```bash
cd ~/embroidery_service_webapp
git pull
pip3.10 install --user -r requirements.txt
# Then reload web app in Web tab
```

---

## Create Update Script (Optional)

Create a convenient update script:

```bash
cd ~/embroidery_service_webapp
nano update.sh
```

Paste this:
```bash
#!/bin/bash
cd ~/embroidery_service_webapp
echo "Pulling latest changes from GitHub..."
git pull
echo "Installing/updating dependencies..."
pip3.10 install --user -r requirements.txt
echo ""
echo "✓ Update complete!"
echo "Now go to Web tab and click Reload button."
```

Make it executable:
```bash
chmod +x update.sh
```

Then update with:
```bash
~/embroidery_service_webapp/update.sh
```

