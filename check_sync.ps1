# Script to check if local and GitHub are in sync
Write-Host "=== Checking Local vs GitHub Sync ===" -ForegroundColor Green
Write-Host ""

# Navigate to project directory
$projectPath = "C:\Users\Julian\embroidery_service_webapp"
Set-Location $projectPath

# Get local commit info
Write-Host "Local Repository:" -ForegroundColor Cyan
$localCommit = git rev-parse HEAD
$localMessage = git log -1 --pretty=format:"%s"
$localDate = git log -1 --pretty=format:"%cd" --date=format:"%Y-%m-%d %H:%M:%S"
Write-Host "  Commit: $localCommit" -ForegroundColor White
Write-Host "  Message: $localMessage" -ForegroundColor White
Write-Host "  Date: $localDate" -ForegroundColor White

Write-Host ""

# Fetch latest from GitHub
Write-Host "Fetching latest from GitHub..." -ForegroundColor Yellow
git fetch origin main 2>&1 | Out-Null

Write-Host ""

# Get remote commit info
Write-Host "GitHub Repository:" -ForegroundColor Cyan
$remoteCommit = git rev-parse origin/main
$remoteMessage = git log -1 --pretty=format:"%s" origin/main
$remoteDate = git log -1 --pretty=format:"%cd" --date=format:"%Y-%m-%d %H:%M:%S" origin/main
Write-Host "  Commit: $remoteCommit" -ForegroundColor White
Write-Host "  Message: $remoteMessage" -ForegroundColor White
Write-Host "  Date: $remoteDate" -ForegroundColor White

Write-Host ""

# Compare
if ($localCommit -eq $remoteCommit) {
    Write-Host "SYNCED: Local and GitHub are the same!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Last commit:" -ForegroundColor White
    Write-Host "  $localMessage" -ForegroundColor Gray
} else {
    Write-Host "NOT SYNCED: Local and GitHub are different!" -ForegroundColor Red
    Write-Host ""
    
    # Check if local is ahead
    $localAhead = git rev-list --count origin/main..main
    if ($localAhead -gt 0) {
        Write-Host "Local is $localAhead commit(s) ahead of GitHub" -ForegroundColor Yellow
        Write-Host "Run: git push origin main" -ForegroundColor Yellow
    }
    
    # Check if remote is ahead
    $remoteAhead = git rev-list --count main..origin/main
    if ($remoteAhead -gt 0) {
        Write-Host "GitHub is $remoteAhead commit(s) ahead of local" -ForegroundColor Yellow
        Write-Host "Run: git pull origin main" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Checking for uncommitted changes..." -ForegroundColor Cyan
git status --short
if ($LASTEXITCODE -eq 0) {
    $status = git status --porcelain
    if ([string]::IsNullOrWhiteSpace($status)) {
        Write-Host "No uncommitted changes" -ForegroundColor Green
    } else {
        Write-Host "You have uncommitted changes:" -ForegroundColor Yellow
        git status --short
    }
}

Write-Host ""

