@echo off
title Python Auto-Installer
color 0B
echo.
echo ========================================
echo   PYTHON AUTO-INSTALLER
echo ========================================
echo.
echo This script will install Python automatically.
echo.
echo.

REM Check if Python is already installed
echo [1/4] Checking if Python is already installed...
python --version >nul 2>&1
if not errorlevel 1 (
    python --version
    echo.
    echo [SUCCESS] Python is already installed!
    echo You can now run start_app.bat
    pause
    exit /b 0
)

py --version >nul 2>&1
if not errorlevel 1 (
    py --version
    echo.
    echo [SUCCESS] Python is already installed!
    echo You can now run start_app.bat
    pause
    exit /b 0
)

echo [X] Python not found. Proceeding with installation...
echo.

REM Method 1: Try winget (Windows 10/11)
echo [2/4] Trying winget (Windows Package Manager)...
winget --version >nul 2>&1
if not errorlevel 1 (
    echo [OK] winget is available. Installing Python...
    echo This may take a few minutes...
    echo.
    winget install Python.Python.3.11 --accept-package-agreements --accept-source-agreements
    if not errorlevel 1 (
        echo.
        echo [SUCCESS] Python installed via winget!
        echo.
        echo Please RESTART Command Prompt and run: python --version
        echo Then you can run start_app.bat
        pause
        exit /b 0
    ) else (
        echo [X] winget installation failed. Trying alternative method...
        echo.
    )
) else (
    echo [X] winget not available. Trying alternative method...
    echo.
)

REM Method 2: Download and install manually
echo [3/4] Downloading Python installer...
echo This may take a few minutes depending on your internet speed...
echo.

REM Get latest Python 3.11 URL (you may need to update this URL)
set PYTHON_URL=https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe
set PYTHON_INSTALLER=python-installer.exe

powershell -Command "Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%PYTHON_INSTALLER%'" >nul 2>&1

if not exist "%PYTHON_INSTALLER%" (
    echo [ERROR] Failed to download Python installer.
    echo.
    echo Please download Python manually from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo [OK] Download complete!
echo.

echo [4/4] Installing Python...
echo This will install Python silently. Please wait...
echo.

REM Install Python silently with PATH addition
"%PYTHON_INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

REM Wait a moment for installation
timeout /t 5 /nobreak >nul

REM Clean up installer
if exist "%PYTHON_INSTALLER%" del "%PYTHON_INSTALLER%"

echo.
echo ========================================
echo   INSTALLATION COMPLETE
echo ========================================
echo.
echo Python has been installed!
echo.
echo IMPORTANT: You need to RESTART Command Prompt for changes to take effect.
echo.
echo To verify installation:
echo 1. Close this window
echo 2. Open a NEW Command Prompt
echo 3. Type: python --version
echo 4. If it works, run: start_app.bat
echo.
pause

