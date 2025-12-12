#!/bin/bash
cd ~/embroidery_service_webapp
echo "🔄 Pulling latest changes from GitHub..."
git pull origin main
echo "📦 Installing/updating dependencies..."
pip3.10 install --user -r requirements.txt
echo ""
echo "✅ Update complete!"
echo "👉 Now go to Web tab and click Reload button."

