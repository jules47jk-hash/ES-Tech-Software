# PythonAnywhere WSGI Configuration File
# Copy this content into your WSGI configuration file in PythonAnywhere dashboard

import sys
import os

# IMPORTANT: Replace 'yourusername' with your actual PythonAnywhere username!
path = '/home/yourusername/embroidery_service_webapp'
if path not in sys.path:
    sys.path.insert(0, path)

# Change to your project directory
os.chdir(path)

# Import your Flask app
# Note: init_db() is already called in app.py when the module loads, so we don't need to call it here
from app import app as application

if __name__ == "__main__":
    application.run()

