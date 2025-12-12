# Quick Push Script Guide

## Using the Push Script

### Run the Script

In PowerShell, navigate to your project and run:

```powershell
cd C:\Users\Julian\embroidery_service_webapp
.\push_to_github.ps1
```

### What the Script Does

1. **Checks Git status** - Shows what files have changed
2. **Asks to add changes** - Stages all modified files
3. **Prompts for commit message** - Or uses default timestamp
4. **Commits changes** - Creates a commit
5. **Pushes to GitHub** - Uploads to your repository

### Example Usage

```powershell
PS C:\Users\Julian\embroidery_service_webapp> .\push_to_github.ps1

=== Push to GitHub ===

✓ Git found: git version 2.x.x

Checking current status...
M  templates/login.html

Add all changes? (Y/N): Y
Staging all changes...
✓ Changes staged

Staged changes:
templates/login.html

Enter commit message (or press Enter for default): Updated login page

Committing changes...
✓ Changes committed

Pushing to GitHub...
✓ Successfully pushed to GitHub!

Next steps:
1. Go to PythonAnywhere
2. Run: ~/embroidery_service_webapp/update.sh
3. Reload web app in Web tab
```

### Manual Alternative

If you prefer to do it manually:

```powershell
cd C:\Users\Julian\embroidery_service_webapp
git add .
git commit -m "Your commit message"
git push origin main
```

### Troubleshooting

**"Git is not recognized"**
- Install Git from https://git-scm.com/download/win
- Restart PowerShell after installation

**"Authentication failed"**
- Use Personal Access Token, not password
- Create token at: GitHub → Settings → Developer settings → Personal access tokens

**"Permission denied"**
- Check repository URL: `git remote -v`
- Verify you have access to the repository

