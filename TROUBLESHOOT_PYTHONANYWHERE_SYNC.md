# Troubleshooting PythonAnywhere Not Updating

## Step 1: Check What PythonAnywhere Has

In PythonAnywhere Bash console, run:

```bash
cd ~/embroidery_service_webapp

# Check current commit
git log -1 --oneline

# Check commit hash
git rev-parse HEAD

# Fetch latest from GitHub
git fetch origin main

# Check what GitHub has
git rev-parse origin/main

# Compare
git log HEAD..origin/main --oneline
```

**Expected:** If PythonAnywhere is behind, you'll see commits listed.

---

## Step 2: Pull Latest Changes

```bash
cd ~/embroidery_service_webapp
git pull origin main
```

If you get conflicts or errors, try:
```bash
git fetch origin
git reset --hard origin/main
```

---

## Step 3: Verify Files Updated

Check if the login.html file has "123":

```bash
grep -n "123" templates/login.html
```

Should show the line with "123" in it.

---

## Step 4: Install Dependencies

```bash
pip3.10 install --user -r requirements.txt
```

---

## Step 5: Reload Web App

1. Go to **"Web"** tab
2. Click big green **"Reload"** button
3. Wait 10-15 seconds

---

## Step 6: Clear Browser Cache

After reloading:
- Press **Ctrl+F5** (hard refresh)
- Or use incognito/private window
- Visit: `https://jules47jk.pythonanywhere.com`

---

## Common Issues

### Issue: "Already up to date" but changes not showing
**Fix:** 
- Clear browser cache (Ctrl+F5)
- Check error log in Web tab
- Verify file was actually updated: `cat templates/login.html | grep 123`

### Issue: Git pull fails
**Fix:**
```bash
git fetch origin
git reset --hard origin/main
```

### Issue: Changes pulled but website still shows old version
**Fix:**
- Make sure you clicked Reload in Web tab
- Check error log for template errors
- Verify file exists: `ls -la templates/login.html`

---

## Quick Check Script

Run this on PythonAnywhere:

```bash
cd ~/embroidery_service_webapp
echo "=== Current Status ==="
echo "Local commit:"
git log -1 --oneline
echo ""
echo "Fetching from GitHub..."
git fetch origin main
echo ""
echo "GitHub commit:"
git log -1 --oneline origin/main
echo ""
echo "Differences:"
git log HEAD..origin/main --oneline
echo ""
echo "Checking login.html for '123':"
grep -n "123" templates/login.html || echo "NOT FOUND - file needs update"
```

