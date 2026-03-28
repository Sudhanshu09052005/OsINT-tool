@echo off
echo ===============================================
echo    BROWSER MODE - QUICK TEST
echo ===============================================
echo.
echo Step 1: Testing if Flask is installed...
python -c "import flask; print('Flask OK: v' + flask.__version__)" 2>nul
if errorlevel 1 (
    echo Flask NOT found! Installing...
    pip install flask
) else (
    echo Flask is installed!
)
echo.
echo Step 2: Creating required folders...
if not exist "templates" mkdir templates
if not exist "reports" mkdir reports
echo Folders created!
echo.
echo Step 3: Testing browser mode...
echo.
echo Starting simplified browser mode...
echo Open your browser to: http://localhost:5000
echo.
python web_app_simple.py
pause
