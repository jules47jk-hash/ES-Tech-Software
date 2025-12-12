#!/usr/bin/env python3
# Test script to verify app can be imported
import sys
import os

# Set the project path
project_path = '/home/jules47jk/embroidery_service_webapp'
sys.path.insert(0, project_path)
os.chdir(project_path)

try:
    print("Attempting to import app...")
    from app import app
    print("SUCCESS: App imported!")
    print(f"App name: {app.name}")
    print("\nRoutes found:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.rule} -> {rule.endpoint}")
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

