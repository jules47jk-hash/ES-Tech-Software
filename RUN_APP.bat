@echo off
title Embroidery Service - Manual Launcher
color 0A
echo.
echo ========================================
echo   EMBROIDERY SERVICE WEBAPP
echo ========================================
echo.
echo This will help you run the application manually.
echo.
echo.

REM Try to find Python
set PYTHON_FOUND=0

echo Checking for Python...
python --version >nul 2>&1
if not errorlevel 1 (
    echo [OK] Python found via 'python' command
    set PYTHON_CMD=python
    set PYTHON_FOUND=1
    goto run_app
)

py --version >nul 2>&1
if not errorlevel 1 (
    echo [OK] Python found via 'py' command
    set PYTHON_CMD=py
    set PYTHON_FOUND=1
    goto run_app
)

echo [X] Python not found in PATH
echo.
echo ========================================
echo   PYTHON NOT FOUND
echo ========================================
echo.
echo Python needs to be installed first.
echo.
echo Please:
echo 1. Open INSTALL_PYTHON.md for detailed instructions
echo 2. Or visit: https://www.python.org/downloads/
echo 3. Install Python and check "Add Python to PATH"
echo 4. Then run this file again
echo.
echo ========================================
echo.
pause
exit /b 1

:run_app
echo.
echo ========================================
echo   STARTING APPLICATION
echo ========================================
echo.
echo The app will open at: http://localhost:5000
echo Press Ctrl+C to stop when done.
echo.
echo.

REM Install dependencies if needed
echo Checking dependencies...
%PYTHON_CMD% -m pip show Flask >nul 2>&1
if errorlevel 1 (
    echo Installing required packages (this may take a minute)...
    %PYTHON_CMD% -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ERROR: Could not install dependencies
        echo Try running manually: %PYTHON_CMD% -m pip install -r requirements.txt
        pause
        exit /b 1
    )
)

echo.
echo Opening browser...
timeout /t 2 /nobreak >nul
start http://localhost:5000

echo.
echo Starting server...
echo.
%PYTHON_CMD% app.py

pause

