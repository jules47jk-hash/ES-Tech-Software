# Git Setup Guide - Update from Your Computer

This guide will help you set up Git so you can push changes from your computer and pull them on PythonAnywhere.

---

## Part 1: Install Git on Your Computer

### Step 1: Download Git
1. Go to: **https://git-scm.com/download/win**
2. Download the Windows installer
3. Run the installer

### Step 2: Install Git
1. Click **"Next"** through the installer
2. **Important:** When you see **"Adjusting your PATH environment"**, select:
   - ✅ **"Git from the command line and also from 3rd-party software"**
3. Keep clicking **"Next"** with default settings
4. Click **"Install"**
5. Click **"Finish"**

### Step 3: Verify Installation
1. Open **PowerShell** or **Command Prompt** (new window)
2. Run:
   ```powershell
   git --version
   ```
3. Should show: `git version 2.x.x`

---

## Part 2: Set Up Git Repository Locally

### Step 1: Initialize Git Repository
Open PowerShell in your project folder:
```powershell
cd C:\Users\Julian\embroidery_service_webapp
git init
```

### Step 2: Configure Git (First Time Only)
```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 3: Add All Files
```powershell
git add .
```

### Step 4: Create First Commit
```powershell
git commit -m "Initial commit"
```

---

## Part 3: Create GitHub Repository

### Step 1: Create GitHub Account (If Needed)
1. Go to: **https://github.com**
2. Sign up for a free account (or log in)

### Step 2: Create New Repository
1. Click **"+"** icon → **"New repository"**
2. Repository name: `embroidery-service-webapp` (or any name)
3. Description: (optional)
4. Choose: **Private** (recommended) or **Public**
5. **DO NOT** check "Initialize with README"
6. Click **"Create repository"**

### Step 3: Get Repository URL
After creating, GitHub will show you commands. Copy the repository URL:
- Your repository URL: `https://github.com/jules47jk-hash/ES-Tech-Software.git`
- Or SSH: `git@github.com:jules47jk-hash/ES-Tech-Software.git`

---

## Part 4: Connect Local Repository to GitHub

### Step 1: Add Remote
In PowerShell (in your project folder):
```powershell
cd C:\Users\Julian\embroidery_service_webapp
git remote add origin https://github.com/jules47jk-hash/ES-Tech-Software.git
```

### Step 2: Push to GitHub
```powershell
git branch -M main
git push -u origin main
```

You'll be prompted for GitHub username and password (use a Personal Access Token, not your password - see below).

---

## Part 5: GitHub Authentication (Personal Access Token)

GitHub no longer accepts passwords. You need a Personal Access Token:

### Step 1: Create Token
1. Go to GitHub → Click your profile → **"Settings"**
2. Scroll down → **"Developer settings"**
3. Click **"Personal access tokens"** → **"Tokens (classic)"**
4. Click **"Generate new token"** → **"Generate new token (classic)"**
5. Note: Give it a name like "PythonAnywhere"
6. Select scopes: ✅ **"repo"** (full control of private repositories)
7. Click **"Generate token"**
8. **COPY THE TOKEN IMMEDIATELY** (you won't see it again!)

### Step 2: Use Token When Pushing
When you run `git push`, use:
- **Username:** Your GitHub username
- **Password:** Paste the Personal Access Token (not your GitHub password)

---

## Part 6: Set Up Git on PythonAnywhere

### Step 1: Clone Repository (First Time)
In PythonAnywhere Bash console:
```bash
cd ~
git clone https://github.com/jules47jk-hash/ES-Tech-Software.git embroidery_service_webapp
```

**Note:** If the folder already exists, you can:
```bash
cd ~/embroidery_service_webapp
git remote add origin https://github.com/jules47jk-hash/ES-Tech-Software.git
git branch -M main
git pull origin main --allow-unrelated-histories
```

### Step 2: Set Up Git Credentials (Optional - For Easier Pulling)
```bash
cd ~/embroidery_service_webapp
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

---

## Part 7: Update Workflow

### From Your Computer (After Making Changes):

1. **Make changes** to your files
2. **Stage changes:**
   ```powershell
   cd C:\Users\Julian\embroidery_service_webapp
   git add .
   ```
   Or stage specific files:
   ```powershell
   git add app.py
   git add templates/login.html
   ```

3. **Commit changes:**
   ```powershell
   git commit -m "Description of changes"
   ```
   Example: `git commit -m "Fixed login page styling"`

4. **Push to GitHub:**
   ```powershell
   git push
   ```
   Enter username and Personal Access Token when prompted

### On PythonAnywhere (Pull Changes):

1. Go to **"Consoles"** tab → **"Bash"**
2. Run:
   ```bash
   cd ~/embroidery_service_webapp
   git pull
   ```
3. Install any new dependencies:
   ```bash
   pip3.10 install --user -r requirements.txt
   ```
4. Go to **"Web"** tab → Click **"Reload"**

---

## Quick Reference Commands

### On Your Computer:
```powershell
# Navigate to project
cd C:\Users\Julian\embroidery_service_webapp

# Check status (what files changed)
git status

# Stage all changes
git add .

# Commit changes
git commit -m "Description"

# Push to GitHub
git push
```

### On PythonAnywhere:
```bash
# Navigate to project
cd ~/embroidery_service_webapp

# Pull latest changes
git pull

# Check what changed
git log --oneline -5

# Install new dependencies
pip3.10 install --user -r requirements.txt
```

---

## Troubleshooting

### "Git is not recognized"
- Git is not installed or not in PATH
- Restart PowerShell after installing Git
- Or use Git Bash instead

### "Authentication failed"
- Use Personal Access Token, not password
- Make sure token has "repo" scope

### "Repository not found"
- Check repository URL is correct
- Make sure repository exists on GitHub
- Check if repository is private and you have access

### "Merge conflicts" on PythonAnywhere
If you get merge conflicts:
```bash
cd ~/embroidery_service_webapp
git stash
git pull
git stash pop
```
Then resolve conflicts manually.

---

## Optional: Create Update Script

Create a file `update.sh` on PythonAnywhere for easier updates:

```bash
cd ~/embroidery_service_webapp
nano update.sh
```

Paste this:
```bash
#!/bin/bash
cd ~/embroidery_service_webapp
echo "Pulling latest changes..."
git pull
echo "Installing dependencies..."
pip3.10 install --user -r requirements.txt
echo "Done! Now reload your web app in the Web tab."
```

Make it executable:
```bash
chmod +x update.sh
```

Then update with:
```bash
~/embroidery_service_webapp/update.sh
```

---

## Summary

**Workflow:**
1. **Edit files** on your computer
2. **Commit:** `git add .` → `git commit -m "message"` → `git push`
3. **On PythonAnywhere:** `git pull` → `pip3.10 install --user -r requirements.txt` → Reload web app

That's it! Your changes are live.

