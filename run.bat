@echo off
echo =========================================
echo   ResumeAI - Starting Application
echo =========================================
echo.

IF NOT EXIST "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found.
    echo Please run setup.bat first.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
echo [OK] Virtual environment activated.
echo.
echo Starting ResumeAI server...
echo Open your browser at: http://127.0.0.1:5000
echo Press Ctrl+C to stop.
echo.
python app.py
pause
