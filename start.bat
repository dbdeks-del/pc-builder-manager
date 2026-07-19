@echo off
chcp 65001 >nul
title PC 플리핑 매니저
echo ========================================
echo   PC 플리핑 매니저 - 시작 중...
echo ========================================
echo.

cd /d "%~dp0"

REM ---- Python 확인 ----
python --version >nul 2>&1
if errorlevel 1 (
    echo [오류] Python이 설치되어 있지 않습니다.
    echo        https://www.python.org/downloads/ 에서 Python 3.10 이상을 설치하세요.
    echo        설치할 때 "Add Python to PATH"를 꼭 체크하세요.
    echo.
    pause
    exit /b 1
)

REM ---- 첫 실행 시에만 의존성 설치 ----
if not exist "backend\.installed" (
    echo [1/2] 필요한 라이브러리 설치 중 ^(최초 1회, 인터넷 필요^)...
    python -m pip install --upgrade pip >nul 2>&1
    python -m pip install -r backend\requirements.txt
    if errorlevel 1 (
        echo [오류] 라이브러리 설치 실패. 인터넷 연결을 확인하세요.
        echo.
        pause
        exit /b 1
    )
    echo done > "backend\.installed"
) else (
    echo [1/2] 라이브러리 설치 확인됨.
)

echo [2/2] 서버 실행 중... 잠시 후 브라우저가 자동으로 열립니다.
echo.

cd backend
python launcher.py

echo.
echo 종료되었습니다.
pause >nul
