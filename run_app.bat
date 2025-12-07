@echo off
echo ===================================================
echo   Fruit Freshness Detector - One-Click Launcher
echo ===================================================
echo.
cd /d "%~dp0"

echo [1/3] Installing/Verifying Dependencies...
pip install -r backend/requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Dependency installation failed!
    echo Please ensure Python is installed and check your internet connection.
    pause
    exit /b %errorlevel%
)
echo Dependencies ready.
echo.

echo [2/3] Opening Frontend...
start frontend/index.html
echo Frontend opened.
echo.

echo [3/3] Starting Backend Server...
echo The server window must remain open for the app to work.
echo Connect to http://127.0.0.1:8000
echo.
cd backend
python -m uvicorn main:app --reload
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Server crashed or failed to start.
    pause
)
