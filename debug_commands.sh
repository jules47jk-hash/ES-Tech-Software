#!/bin/bash
# Run these commands one by one in PythonAnywhere Bash console

echo "=== 1. Check project location ==="
cd ~/embroidery_service_webapp
pwd
ls -la

echo ""
echo "=== 2. Check WSGI file ==="
cat /var/www/jules47jk_pythonanywhere_com_wsgi.py

echo ""
echo "=== 3. Test app import ==="
cd ~/embroidery_service_webapp
python3.10 -c "import sys; sys.path.insert(0, '/home/jules47jk/embroidery_service_webapp'); import os; os.chdir('/home/jules47jk/embroidery_service_webapp'); from app import app; print('SUCCESS: App imported!'); print('Routes:', [r.rule for r in app.url_map.iter_rules()][:5])"

echo ""
echo "=== 4. Check database ==="
cd ~/embroidery_service_webapp
ls -la service.db 2>&1

echo ""
echo "=== 5. Check packages ==="
pip3.10 list | grep -i flask

