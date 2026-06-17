@echo off
title PC Builder Manager
echo ========================================
echo   PC Builder Manager - Starting...
echo ========================================
echo.

cd /d "%~dp0"

echo [1/2] Starting backend server...
start "PC Builder Backend" cmd /k "cd backend && python -m uvicorn main:app --reload --port 8000"

echo [2/2] Opening browser...
timeout /t 2 /nobreak >nul
start "" "frontend\index.html"

echo.
echo ✅ PC Builder Manager is running!
echo    Backend: http://localhost:8000
echo    Frontend: Open in browser
echo.
echo Press any key to stop all services...
pause >nul

taskkill /f /fi "WINDOWTITLE eq PC Builder Backend" >nul 2>&1
echo Stopped.
