#!/bin/bash
# Update script for PythonAnywhere
# Pulls latest changes from GitHub and reloads dependencies

cd ~/embroidery_service_webapp

echo "🔄 Pulling latest changes from GitHub..."
git fetch origin main

# Check if there are updates
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)

if [ "$LOCAL" = "$REMOTE" ]; then
    echo "✅ Already up to date!"
else
    echo "📥 New changes found. Pulling..."
    git reset --hard origin/main
    
    if [ $? -eq 0 ]; then
        echo "✅ Successfully pulled latest changes"
    else
        echo "❌ Error pulling changes. Trying merge instead..."
        git pull origin main
    fi
fi

echo ""
echo "📦 Installing/updating dependencies..."
pip3.10 install --user -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies updated"
else
    echo "⚠️  Some dependencies may have failed to install"
fi

echo ""
echo "📋 Current commit:"
git log -1 --oneline

echo ""
echo "✅ Update complete!"
echo ""
echo "👉 Next step: Go to Web tab and click Reload button"
