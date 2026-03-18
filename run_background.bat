@echo off
echo ===============================================
echo   ResumeAI - Starting Server in Background
echo ===============================================
echo.

IF NOT EXIST "venv\Scripts\pythonw.exe" (
    echo [ERROR] Virtual environment not found or pythonw missing.
    echo Please make sure the venv is properly set up.
    pause
    exit /b 1
)

echo Starting ResumeAI server silently...
start "" "venv\Scripts\pythonw.exe" "app.py"

echo [OK] Server is running in the background.
echo You can now access: http://127.0.0.1:5000
echo You can safely close this terminal, Antigravity, or IDE. The server will stay running 24/7.
echo.
echo To stop the server later, simply run "stop_server.bat"
pause
