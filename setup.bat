@echo off
echo =========================================
echo   ResumeAI - Automated Setup Script
echo =========================================
echo.

:: Check for 'py' launcher or 'python'
set PY_CMD=python
py --version >nul 2>&1
if %ERRORLEVEL% == 0 (
    set PY_CMD=py
) else (
    python --version >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Python is not installed or not on PATH.
        echo Please install Python 3.9+ from https://www.python.org/downloads/
        echo Make sure to check "Add Python to PATH" during installation.
        pause
        exit /b 1
    )
)

echo [OK] Using command: %PY_CMD%
%PY_CMD% --version

echo.
echo [1/4] Creating virtual environment...
%PY_CMD% -m venv venv
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to create virtual environment.
    pause
    exit /b 1
)

echo [2/4] Activating virtual environment & Updating Pip...
call venv\Scripts\activate.bat
:: Upgrade pip, setuptools and wheel first to handle modern wheels/metadata
python -m pip install --upgrade pip setuptools wheel

echo [3/4] Installing dependencies...
:: Switching to pypdf (pure Python) to avoid build errors on newer Python versions
pip install Flask==3.0.0 pypdf==4.0.1 python-docx==1.1.0 spacy==3.7.2 Werkzeug==3.0.1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install dependencies.
    echo Trying alternative install without specific versions...
    pip install Flask pypdf python-docx spacy Werkzeug
)

IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Still failing. Please ensure your Python installation is complete.
    pause
    exit /b 1
)

echo [4/4] Downloading spaCy English language model...
python -m pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1.tar.gz
IF %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Could not download spaCy model automatically.
    echo Please run: python -m spacy download en_core_web_sm
)

echo.
echo =========================================
echo   Setup Complete!
echo.
echo   To start the application, run:
echo   run.bat
echo =========================================
echo.
pause
