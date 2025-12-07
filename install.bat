@echo off
echo ========================================
echo   Transcript CLI Installer
echo ========================================
echo.

:: Get the directory where this batch file is located
set "INSTALL_DIR=%~dp0"
cd /d "%INSTALL_DIR%"

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python 3.10+ and add it to PATH.
    pause
    exit /b 1
)

:: Check if venv exists, create if not
if not exist "venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo.
    
    echo Installing dependencies...
    venv\Scripts\pip install requests python-dotenv pydub
    if errorlevel 1 (
        echo Error: Failed to install dependencies.
        pause
        exit /b 1
    )
    echo.
)

:: Run the Python installer to update paths
echo Updating transcript.cmd paths...
venv\Scripts\python.exe install.py

echo.
echo ========================================
echo   Installation Complete!
echo ========================================
echo.
echo Don't forget to:
echo   1. Add "%INSTALL_DIR%transcript_bin" to your system PATH
echo   2. Create a .env file with your SONIOX_API_KEY
echo.
pause
