@echo off
echo ===============================================
echo    WHOIS FIX - Installing Correct Package
echo ===============================================
echo.
echo Step 1: Removing old whois package...
pip uninstall whois -y
echo.
echo Step 2: Installing python-whois...
pip install python-whois
echo.
echo ===============================================
echo    Installation Complete!
echo ===============================================
echo.
echo Now you can run the tool normally.
echo.
pause
