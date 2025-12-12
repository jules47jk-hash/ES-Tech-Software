#!/bin/bash
# Manual update script - runs commands directly without requiring execute permissions
# Usage: bash ~/embroidery_service_webapp/update_manual.sh

cd ~/embroidery_service_webapp || {
    echo "❌ Error: Cannot change to project directory"
    exit 1
}

echo "📁 Current directory: $(pwd)"
echo ""

# Backup database before update (optional safety measure)
if [ -f "service.db" ]; then
    echo "💾 Database found - creating backup..."
    BACKUP_NAME="service.db.backup.$(date +%Y%m%d_%H%M%S)"
    if cp service.db "$BACKUP_NAME" 2>/dev/null; then
        echo "✅ Database backed up as: $BACKUP_NAME"
    else
        echo "⚠️  Could not backup database (may not have write permissions)"
    fi
else
    echo "ℹ️  No database found - will be created on first run"
fi

echo ""
echo "🔄 Pulling latest changes from GitHub..."

# Fetch latest changes
if ! git fetch origin main 2>&1; then
    echo "❌ Error: Cannot fetch from GitHub"
    echo "   Check your internet connection and git configuration"
    exit 1
fi

# Check if there are updates
LOCAL=$(git rev-parse HEAD 2>/dev/null)
REMOTE=$(git rev-parse origin/main 2>/dev/null)

if [ "$LOCAL" = "$REMOTE" ]; then
    echo "✅ Already up to date!"
else
    echo "📥 New changes found. Pulling..."
    
    # Backup database before reset
    if [ -f "service.db" ]; then
        DB_BACKUP="service.db.backup.temp"
        cp service.db "$DB_BACKUP" 2>/dev/null || true
    fi
    
    # Try reset first (cleaner)
    if git reset --hard origin/main 2>&1; then
        echo "✅ Successfully reset to latest version"
        
        # Restore database if it was backed up
        if [ -f "$DB_BACKUP" ]; then
            if mv "$DB_BACKUP" service.db 2>/dev/null; then
                echo "✅ Database preserved"
            else
                echo "⚠️  Could not restore database backup"
            fi
        fi
    else
        echo "⚠️  Reset failed, trying merge instead..."
        
        # Restore database backup before merge
        if [ -f "$DB_BACKUP" ]; then
            mv "$DB_BACKUP" service.db 2>/dev/null || true
        fi
        
        # Try merge
        if git pull origin main 2>&1; then
            echo "✅ Successfully merged latest changes"
        else
            echo "❌ Error: Both reset and merge failed"
            echo "   You may need to resolve conflicts manually"
            exit 1
        fi
    fi
fi

echo ""
echo "📦 Installing/updating dependencies..."

if pip3.10 install --user -r requirements.txt 2>&1; then
    echo "✅ Dependencies updated"
else
    echo "⚠️  Some dependencies may have failed to install"
    echo "   Check the error messages above"
fi

echo ""
echo "📋 Current commit:"
git log -1 --oneline 2>/dev/null || echo "Could not get commit info"

echo ""
echo "✅ Update complete!"
echo ""
echo "👉 Next step: Go to Web tab in PythonAnywhere and click Reload button"

