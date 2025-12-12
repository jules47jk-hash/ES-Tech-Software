# Server Deployment Guide

## Overview

This guide covers deploying your Flask application to a purchased server (VPS, cloud server, etc.).

---

## Option 1: Simple Production Server (Recommended for Start)

### Requirements
- Server with Ubuntu/Debian Linux (most common)
- SSH access
- Python 3.8+ installed

### Step-by-Step Deployment

#### 1. Connect to Your Server
```bash
ssh username@your-server-ip
```

#### 2. Install Python and Dependencies
```bash
# Update system
sudo apt update
sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Install other tools
sudo apt install git nginx -y
```

#### 3. Upload Your Application
**Option A: Using Git (Recommended)**
```bash
# On your local machine, create a git repository
git init
git add .
git commit -m "Initial commit"

# Push to GitHub/GitLab
# Then on server:
git clone https://github.com/yourusername/embroidery-service.git
cd embroidery-service
```

**Option B: Using SCP (Direct Upload)**
```bash
# From your local machine:
scp -r C:\Users\Julian\embroidery_service_webapp username@your-server-ip:/home/username/
```

**Option C: Using SFTP Client**
- Use FileZilla, WinSCP, or similar
- Upload entire folder to server

#### 4. Set Up Python Environment
```bash
cd embroidery-service-webapp  # or your folder name

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install production server
pip install gunicorn
```

#### 5. Configure the Application

Edit `app.py` to remove debug mode:
```python
# Change line 1397 from:
if __name__ == "__main__":
    init_db()
    app.run(debug=True)

# To:
if __name__ == "__main__":
    init_db()
    # Don't run app here in production
```

#### 6. Test the Application
```bash
# Run with Gunicorn to test
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# If it works, press Ctrl+C to stop
```

#### 7. Create Systemd Service (Auto-start)

Create service file:
```bash
sudo nano /etc/systemd/system/embroidery-service.service
```

Add this content:
```ini
[Unit]
Description=Embroidery Service Webapp
After=network.target

[Service]
User=your-username
Group=www-data
WorkingDirectory=/home/your-username/embroidery-service-webapp
Environment="PATH=/home/your-username/embroidery-service-webapp/venv/bin"
ExecStart=/home/your-username/embroidery-service-webapp/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

**Replace:**
- `your-username` with your actual username
- Paths to match your setup

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable embroidery-service
sudo systemctl start embroidery-service
sudo systemctl status embroidery-service
```

#### 8. Set Up Nginx Reverse Proxy

Create Nginx config:
```bash
sudo nano /etc/nginx/sites-available/embroidery-service
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;  # or your-server-ip

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files (if needed)
    location /static {
        alias /home/your-username/embroidery-service-webapp/static;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/embroidery-service /etc/nginx/sites-enabled/
sudo nginx -t  # Test configuration
sudo systemctl restart nginx
```

#### 9. Set Up SSL (HTTPS) - Optional but Recommended

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is set up automatically
```

---

## Option 2: Using Waitress (Windows Server)

If your server is Windows:

### Install Waitress
```bash
pip install waitress
```

### Create a startup script `start_production.py`:
```python
from waitress import serve
from app import app, init_db

if __name__ == '__main__':
    init_db()
    # Serve on all interfaces, port 5000
    serve(app, host='0.0.0.0', port=5000)
```

### Run it:
```bash
python start_production.py
```

### Set up as Windows Service (Optional)
Use NSSM (Non-Sucking Service Manager) to run as a service.

---

## Option 3: Cloud Platform Deployment

### Heroku (Easiest - Free tier available)

1. **Install Heroku CLI** from heroku.com
2. **Create `Procfile`** in your app folder:
   ```
   web: gunicorn app:app
   ```
3. **Create `runtime.txt`**:
   ```
   python-3.11.7
   ```
4. **Deploy**:
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   heroku open
   ```

### PythonAnywhere (Beginner-friendly)

1. Sign up at pythonanywhere.com
2. Upload files via web interface
3. Configure web app in dashboard
4. Set WSGI file to point to your app

### DigitalOcean App Platform

1. Connect GitHub repository
2. Select Python buildpack
3. Auto-deploys on git push

---

## Security Checklist

- [ ] Change `app.secret_key` to a strong random string
- [ ] Set `debug=False` in production
- [ ] Use environment variables for sensitive data
- [ ] Set up firewall (only allow ports 80, 443, 22)
- [ ] Use HTTPS (SSL certificate)
- [ ] Keep server updated: `sudo apt update && sudo apt upgrade`
- [ ] Set up regular database backups
- [ ] Use strong passwords/SSH keys
- [ ] Consider adding authentication to the app

---

## Database Backup Strategy

### Automated Backup Script

Create `backup_db.sh`:
```bash
#!/bin/bash
BACKUP_DIR="/home/your-username/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR
cp /home/your-username/embroidery-service-webapp/service.db $BACKUP_DIR/service_$DATE.db
# Keep only last 30 days
find $BACKUP_DIR -name "service_*.db" -mtime +30 -delete
```

Make it executable:
```bash
chmod +x backup_db.sh
```

Add to crontab (daily backup at 2 AM):
```bash
crontab -e
# Add this line:
0 2 * * * /home/your-username/backup_db.sh
```

---

## Environment Variables (Recommended)

Create `.env` file (don't commit to git):
```env
SECRET_KEY=your-super-secret-key-here
FLASK_ENV=production
```

Update `app.py` to use it:
```python
import os
from dotenv import load_dotenv

load_dotenv()
app.secret_key = os.getenv('SECRET_KEY', 'change_this_secret_key')
```

Install python-dotenv:
```bash
pip install python-dotenv
```

---

## Monitoring & Logs

### View Application Logs
```bash
sudo journalctl -u embroidery-service -f
```

### View Nginx Logs
```bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

---

## Quick Commands Reference

```bash
# Restart application
sudo systemctl restart embroidery-service

# Check status
sudo systemctl status embroidery-service

# View logs
sudo journalctl -u embroidery-service -n 50

# Restart Nginx
sudo systemctl restart nginx

# Update application (after git pull)
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart embroidery-service
```

---

## Troubleshooting

### Application won't start
- Check logs: `sudo journalctl -u embroidery-service`
- Verify paths in service file
- Check file permissions

### 502 Bad Gateway
- Check if app is running: `sudo systemctl status embroidery-service`
- Check if port 5000 is correct in Nginx config
- Check firewall settings

### Can't access from browser
- Check firewall: `sudo ufw status`
- Verify Nginx is running: `sudo systemctl status nginx`
- Check domain DNS settings

---

## Recommended Server Providers

1. **DigitalOcean** - $6/month, great docs
2. **Linode** - $5/month, reliable
3. **Vultr** - $6/month, good performance
4. **AWS Lightsail** - $3.50/month, scalable
5. **Hetzner** - €4/month, Europe-based

---

## Next Steps

1. Choose your server provider
2. Set up server (Ubuntu recommended)
3. Follow Option 1 steps above
4. Point your domain to server IP
5. Set up SSL certificate
6. Test thoroughly before going live

