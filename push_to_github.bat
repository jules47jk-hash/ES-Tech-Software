@echo off
REM Batch file to push code to GitHub
REM This bypasses PowerShell execution policy

echo === Push to GitHub ===
echo.

cd /d "C:\Users\Julian\embroidery_service_webapp"

REM Run PowerShell script with bypass execution policy
powershell.exe -ExecutionPolicy Bypass -File "%~dp0push_to_github.ps1"

pause

