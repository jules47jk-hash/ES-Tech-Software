#!/bin/bash
# Update script for PythonAnywhere
# Pulls latest changes from GitHub and reloads dependencies
# IMPORTANT: Database files are preserved and will NOT be overwritten

cd ~/embroidery_service_webapp

# Backup database before update (optional safety measure)
if [ -f "service.db" ]; then
    echo "💾 Database found - it will be preserved during update"
    cp service.db service.db.backup.$(date +%Y%m%d_%H%M%S) 2>/dev/null || true
fi

echo "🔄 Pulling latest changes from GitHub..."
git fetch origin main

# Check if there are updates
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)

if [ "$LOCAL" = "$REMOTE" ]; then
    echo "✅ Already up to date!"
else
    echo "📥 New changes found. Pulling..."
    
    # Stash database files to preserve them (they're in .gitignore but being extra safe)
    if [ -f "service.db" ]; then
        DB_BACKUP="service.db.backup.temp"
        cp service.db "$DB_BACKUP" 2>/dev/null || true
    fi
    
    git reset --hard origin/main
    
    # Restore database if it was backed up
    if [ -f "$DB_BACKUP" ]; then
        mv "$DB_BACKUP" service.db 2>/dev/null || true
        echo "✅ Database preserved"
    fi
    
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
