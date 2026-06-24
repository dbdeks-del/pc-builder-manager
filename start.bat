@echo off
chcp 65001 >nul
title PC Builder Manager
echo ========================================
echo   PC Builder Manager - Starting...
echo ========================================
echo.

cd /d "%~dp0"

REM ---- Check Python ----
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo         Install Python 3.10+ from https://www.python.org/downloads/
    echo         Be sure to check "Add Python to PATH" during install.
    echo.
    pause
    exit /b 1
)

REM ---- Install dependencies on first run ----
if not exist "backend\.installed" (
    echo [1/3] Installing dependencies ^(first run only^)...
    python -m pip install --upgrade pip >nul 2>&1
    python -m pip install -r backend\requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies. Check your internet connection.
        echo.
        pause
        exit /b 1
    )
    echo done > "backend\.installed"
) else (
    echo [1/3] Dependencies already installed.
)

echo [2/3] Starting backend server...
start "PC Builder Backend" cmd /k "cd /d "%~dp0backend" && python -m uvicorn main:app --reload --port 8000"

echo [3/3] Opening browser...
timeout /t 3 /nobreak >nul
start "" "frontend\index.html"

echo.
echo PC Builder Manager is running!
echo    Backend: http://localhost:8000
echo    Frontend: opened in your browser
echo.
echo Press any key to stop all services...
pause >nul

taskkill /f /fi "WINDOWTITLE eq PC Builder Backend" >nul 2>&1
echo Stopped.
