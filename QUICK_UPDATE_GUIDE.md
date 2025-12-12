# Quick Update Guide - Git Workflow

## ✅ Setup Complete!

Your Git is now configured. Here's how to update your app:

---

## 🔄 Update Workflow

### **From Your Computer (After Making Changes):**

1. **Make your changes** to files locally
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
   git commit -m "Description of what you changed"
   ```
   Examples:
   - `git commit -m "Fixed login page styling"`
   - `git commit -m "Added new part to catalog"`
   - `git commit -m "Updated job export template"`

4. **Push to GitHub:**
   ```powershell
   git push
   ```
   Enter your GitHub username and Personal Access Token when prompted

### **On PythonAnywhere (To Get Updates):**

1. **Open Bash console:**
   - Go to PythonAnywhere → **"Consoles"** tab → **"Bash"**

2. **Pull latest changes:**
   ```bash
   cd ~/embroidery_service_webapp
   git pull
   ```

3. **Install any new dependencies:**
   ```bash
   pip3.10 install --user -r requirements.txt
   ```

4. **Reload web app:**
   - Go to **"Web"** tab → Click big green **"Reload"** button

5. **Test your changes:**
   - Visit: `https://jules47jk.pythonanywhere.com`

---

## 🚀 Quick Update Script (Optional)

Create a script to make updates easier on PythonAnywhere:

```bash
cd ~/embroidery_service_webapp
nano update.sh
```

Paste this:
```bash
#!/bin/bash
cd ~/embroidery_service_webapp
echo "🔄 Pulling latest changes from GitHub..."
git pull
echo "📦 Installing/updating dependencies..."
pip3.10 install --user -r requirements.txt
echo ""
echo "✅ Update complete!"
echo "👉 Now go to Web tab and click Reload button."
```

Save (Ctrl+X, then Y, then Enter), then make it executable:
```bash
chmod +x update.sh
```

Then update with just:
```bash
~/embroidery_service_webapp/update.sh
```

---

## 📋 Common Commands Reference

### On Your Computer:
```powershell
# Check what files changed
git status

# Stage all changes
git add .

# Commit
git commit -m "Your message"

# Push to GitHub
git push
```

### On PythonAnywhere:
```bash
# Pull latest changes
cd ~/embroidery_service_webapp
git pull

# Check what changed
git log --oneline -5

# Install dependencies
pip3.10 install --user -r requirements.txt
```

---

## ⚠️ Important Notes

1. **Always commit and push from your computer first** before pulling on PythonAnywhere
2. **Always reload the web app** after pulling changes
3. **Backup your database** before major updates (download `service.db` from Files tab)
4. **Test changes** on the live site after updating

---

## 🎯 Example Workflow

**Scenario: You fixed a bug in app.py**

1. **On your computer:**
   ```powershell
   cd C:\Users\Julian\embroidery_service_webapp
   git add app.py
   git commit -m "Fixed bug in job listing"
   git push
   ```

2. **On PythonAnywhere:**
   ```bash
   cd ~/embroidery_service_webapp
   git pull
   # Then reload web app
   ```

3. **Done!** Your fix is live! 🎉

---

## 🆘 Troubleshooting

### "Your branch is behind"
```bash
git pull
```

### "Merge conflicts"
```bash
git stash
git pull
git stash pop
# Then resolve conflicts manually
```

### Changes not showing
- Clear browser cache (Ctrl+F5)
- Make sure you reloaded the web app
- Check error log in Web tab

---

That's it! You're all set up! 🎊

