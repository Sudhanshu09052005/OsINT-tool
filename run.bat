@echo off
REM OSINT Tool Quick Start for Windows

echo.
echo ============================================================
echo   OSINT Web Reconnaissance Tool - Setup & Launch
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org
    pause
    exit /b 1
)

echo [*] Python is installed
python --version

echo.
echo [*] Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [+] Dependencies installed successfully!
echo.
echo [*] Launching OSINT Tool...
python osint_tool.py

pause
