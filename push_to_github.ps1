# PowerShell script to push code to GitHub
Write-Host "=== Push to GitHub ===" -ForegroundColor Green
Write-Host ""

# Navigate to project directory
$projectPath = "C:\Users\Julian\embroidery_service_webapp"
Set-Location $projectPath

# Check if Git is available
$gitCheck = git --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Git is not installed or not in PATH!" -ForegroundColor Red
    Write-Host "Please install Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit
}
Write-Host "Git found: $gitCheck" -ForegroundColor Green

Write-Host ""
Write-Host "Checking current status..." -ForegroundColor Yellow
git status --short

Write-Host ""

# Check if there are uncommitted changes
git diff --quiet
$hasUncommitted = $LASTEXITCODE -ne 0

# Check if there are staged changes
git diff --cached --quiet
$hasStaged = $LASTEXITCODE -ne 0

# Check if there are commits to push
$commitsAhead = 0
$checkAhead = git rev-list --count origin/main..main 2>&1
if ($LASTEXITCODE -eq 0) {
    $commitsAhead = [int]$checkAhead
}

# If no changes and no commits to push
if (-not $hasUncommitted -and -not $hasStaged -and $commitsAhead -eq 0) {
    Write-Host "Everything is up to date!" -ForegroundColor Green
    exit
}

# If there are commits ready to push but no new changes
if (-not $hasUncommitted -and -not $hasStaged -and $commitsAhead -gt 0) {
    Write-Host "Found $commitsAhead commit(s) ready to push." -ForegroundColor Cyan
    Write-Host ""
    $push = Read-Host "Push to GitHub? (Y/N)"
    if ($push -eq "Y" -or $push -eq "y") {
        git push origin main
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "Successfully pushed to GitHub!" -ForegroundColor Green
        } else {
            Write-Host ""
            Write-Host "Push failed. Check error messages above." -ForegroundColor Red
        }
    }
    exit
}

# Ask if user wants to add all changes
Write-Host ""
$addAll = Read-Host "Add all changes? (Y/N)"
if ($addAll -eq "Y" -or $addAll -eq "y") {
    Write-Host "Staging all changes..." -ForegroundColor Yellow
    git add .
    Write-Host "Changes staged" -ForegroundColor Green
} else {
    Write-Host "Skipping staging. Only pushing existing commits." -ForegroundColor Yellow
}

# Check if there are staged changes to commit
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Staged changes:" -ForegroundColor Cyan
    git diff --cached --name-only
    
    Write-Host ""
    $commitMessage = Read-Host "Enter commit message (or press Enter for default)"
    
    if ([string]::IsNullOrWhiteSpace($commitMessage)) {
        $dateStr = Get-Date -Format "yyyy-MM-dd HH:mm"
        $commitMessage = "Update code - $dateStr"
    }
    
    Write-Host ""
    Write-Host "Committing changes..." -ForegroundColor Yellow
    git commit -m $commitMessage
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Changes committed" -ForegroundColor Green
    } else {
        Write-Host "Commit failed" -ForegroundColor Red
        exit
    }
}

# Push to GitHub
Write-Host ""
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Successfully pushed to GitHub!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Go to PythonAnywhere" -ForegroundColor White
    Write-Host "2. Run: ~/embroidery_service_webapp/update.sh" -ForegroundColor White
    Write-Host "3. Reload web app in Web tab" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "Push failed. Check error messages above." -ForegroundColor Red
    Write-Host ""
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "- Authentication: Use Personal Access Token, not password" -ForegroundColor White
    Write-Host "- Network: Check your internet connection" -ForegroundColor White
    Write-Host "- Permissions: Verify you have access to the repository" -ForegroundColor White
}
