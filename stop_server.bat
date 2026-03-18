@echo off
echo ===============================================
echo   ResumeAI - Stopping Background Server
echo ===============================================
echo.
echo Stopping the application running in the background...

:: This command looks for pythonw.exe processes running app.py and terminates them
wmic process where "name='pythonw.exe' and commandline like '%%app.py%%'" call terminate >nul 2>&1

echo [OK] Server stopped successfully.
pause
