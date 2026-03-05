@echo off
REM ============================================================
REM  MadeInTracker - Windows Setup Script
REM  Requires Python 3.10 or newer
REM ============================================================

echo [1/4] Checking Python version...
python --version 2>NUL
IF ERRORLEVEL 1 (
    echo ERROR: Python not found. Please install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

echo [2/4] Creating virtual environment...
python -m venv .venv
IF ERRORLEVEL 1 (
    echo ERROR: Failed to create virtual environment.
    pause
    exit /b 1
)

echo [3/4] Activating virtual environment...
call .venv\Scripts\activate.bat

echo [4/4] Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

IF ERRORLEVEL 1 (
    echo.
    echo ERROR: Some packages failed to install.
    echo Make sure you are using Python 3.10+ and have internet access.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo  Setup complete! To start the project:
echo    1. Activate the venv:   .venv\Scripts\activate
echo    2. Copy .env.example to .env and fill in your API keys
echo    3. Run:                  python main.py
echo ============================================================
pause
