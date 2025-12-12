# Final Verification Steps

## Step 1: Verify App Import

Run this in Bash:
```bash
cd ~/embroidery_service_webapp
python3.10 -c "from app import app; print('SUCCESS'); print('Routes:', len([r for r in app.url_map.iter_rules()]), 'routes found')"
```

Should show many routes (not just 2).

---

## Step 2: Check Dependencies

```bash
pip3.10 list | grep -i flask
```

Should show:
- Flask
- Flask-Login

If Flask-Login is missing:
```bash
pip3.10 install --user Flask-Login==0.6.3
```

---

## Step 3: Reload Web App

1. Go to **"Web"** tab
2. Click the big green **"Reload"** button
3. Wait a few seconds

---

## Step 4: Check Error Log

1. Go to **"Web"** tab
2. Click **"Error log"** link
3. Check for any errors

---

## Step 5: Visit Your Site

Visit: `https://jules47jk.pythonanywhere.com`

You should see:
- ✅ **Login page** (not "Hello from Flask!")
- Username: `Fairfield`
- Password: `ES2025`

---

## If Still Seeing "Hello from Flask!"

1. **Clear browser cache** (Ctrl+F5 or Ctrl+Shift+R)
2. **Try incognito/private window**
3. **Check error log** for specific errors
4. **Verify WSGI file** still has correct content:
   ```bash
   cat /var/www/jules47jk_pythonanywhere_com_wsgi.py
   ```

---

## Common Issues

### Missing Flask-Login
```bash
pip3.10 install --user Flask-Login==0.6.3
```

### Database Permission Error
```bash
cd ~/embroidery_service_webapp
chmod 666 service.db
```

### Template Not Found
- Make sure `templates/` folder has all HTML files
- Check `templates/login.html` exists

