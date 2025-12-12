# Git Setup Script for Windows
# Run this in PowerShell: .\setup_git.ps1

Write-Host "=== Git Setup for Embroidery Service Webapp ===" -ForegroundColor Green
Write-Host ""

# Check if Git is installed
Write-Host "Checking if Git is installed..." -ForegroundColor Yellow
try {
    $gitVersion = git --version
    Write-Host "✓ Git is installed: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Git is not installed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host "Then run this script again." -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "=== Initializing Git Repository ===" -ForegroundColor Green

# Check if already a git repository
if (Test-Path .git) {
    Write-Host "✓ Git repository already initialized" -ForegroundColor Green
} else {
    Write-Host "Initializing Git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✓ Git repository initialized" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== Checking Git Configuration ===" -ForegroundColor Green

$userName = git config --global user.name
$userEmail = git config --global user.email

if ($userName -and $userEmail) {
    Write-Host "✓ Git configured:" -ForegroundColor Green
    Write-Host "  Name: $userName" -ForegroundColor Cyan
    Write-Host "  Email: $userEmail" -ForegroundColor Cyan
} else {
    Write-Host "⚠ Git not configured. Please run:" -ForegroundColor Yellow
    Write-Host "  git config --global user.name `"Your Name`"" -ForegroundColor Cyan
    Write-Host "  git config --global user.email `"your.email@example.com`"" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "=== Checking Repository Status ===" -ForegroundColor Green
git status --short

Write-Host ""
Write-Host "=== Next Steps ===" -ForegroundColor Green
Write-Host "1. Create a repository on GitHub (https://github.com)" -ForegroundColor Yellow
Write-Host "2. Add remote: git remote add origin https://github.com/yourusername/repo-name.git" -ForegroundColor Yellow
Write-Host "3. First commit: git add ." -ForegroundColor Yellow
Write-Host "4. Commit: git commit -m `"Initial commit`"" -ForegroundColor Yellow
Write-Host "5. Push: git push -u origin main" -ForegroundColor Yellow
Write-Host ""
Write-Host "See GIT_SETUP_GUIDE.md for detailed instructions!" -ForegroundColor Cyan

