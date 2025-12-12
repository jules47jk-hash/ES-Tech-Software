@echo off
echo ========================================
echo Embroidery Service Webapp
echo ========================================
echo.

REM Check if Python is installed (try both 'python' and 'py')
set PYTHON_CMD=
python --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python
    goto python_found
)

py --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py
    goto python_found
)

REM Try common Python installation paths
if exist "C:\Python39\python.exe" (
    set PYTHON_CMD=C:\Python39\python.exe
    goto python_found
)
if exist "C:\Python310\python.exe" (
    set PYTHON_CMD=C:\Python310\python.exe
    goto python_found
)
if exist "C:\Python311\python.exe" (
    set PYTHON_CMD=C:\Python311\python.exe
    goto python_found
)
if exist "C:\Python312\python.exe" (
    set PYTHON_CMD=C:\Python312\python.exe
    goto python_found
)
if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python39\python.exe" (
    set PYTHON_CMD=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python39\python.exe
    goto python_found
)
if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe" (
    set PYTHON_CMD=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe
    goto python_found
)
if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe" (
    set PYTHON_CMD=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe
    goto python_found
)
if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" (
    set PYTHON_CMD=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe
    goto python_found
)

echo ========================================
echo ERROR: Python is not installed or not in PATH
echo ========================================
echo.
echo Python is required to run this application.
echo.
echo INSTALLATION INSTRUCTIONS:
echo.
echo 1. Download Python from: https://www.python.org/downloads/
echo 2. Run the installer
echo 3. IMPORTANT: Check the box "Add Python to PATH" during installation
echo 4. Click "Install Now"
echo 5. After installation, close this window and run start_app.bat again
echo.
echo ========================================
echo.
echo If Python is already installed but not found:
echo - Try restarting your computer after installation
echo - Or manually add Python to PATH (see README_SETUP.md)
echo.
pause
exit /b 1

:python_found
echo Python found! (Using: %PYTHON_CMD%)
echo.

REM Check if requirements are installed
echo Checking dependencies...
%PYTHON_CMD% -m pip show Flask >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    %PYTHON_CMD% -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        echo Try running manually: %PYTHON_CMD% -m pip install -r requirements.txt
        pause
        exit /b 1
    )
) else (
    echo Dependencies already installed.
)

echo.
echo Starting application...
echo.
echo The application will open in your browser at http://localhost:5000
echo Press Ctrl+C to stop the application
echo.

REM Start the application
start http://localhost:5000
%PYTHON_CMD% app.py

pause

