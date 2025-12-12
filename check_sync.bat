@echo off
REM Batch file to check sync status
powershell.exe -ExecutionPolicy Bypass -File "%~dp0check_sync.ps1"
pause

