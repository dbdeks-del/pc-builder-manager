@echo off
chcp 65001 >nul
title PC 플리핑 매니저 - 실행파일 빌드
echo ========================================
echo   PC 플리핑 매니저 - 실행파일(.exe) 빌드
echo ========================================
echo.

cd /d "%~dp0backend"

python --version >nul 2>&1
if errorlevel 1 (
    echo [오류] Python이 설치되어 있지 않습니다.
    echo        https://www.python.org/downloads/ 에서 Python 3.10 이상을 설치하세요.
    pause
    exit /b 1
)

echo [1/3] 빌드 도구 설치 중 ^(인터넷 필요^)...
python -m pip install --upgrade pip >nul 2>&1
python -m pip install -r requirements.txt pyinstaller
if errorlevel 1 (
    echo [오류] 설치 실패. 인터넷 연결을 확인하세요.
    pause
    exit /b 1
)

echo [2/3] PyInstaller로 빌드 중 ^(수 분 소요될 수 있습니다^)...
python -m PyInstaller pc_flipping_manager.spec --noconfirm
if errorlevel 1 (
    echo [오류] 빌드 실패.
    pause
    exit /b 1
)

echo [3/3] 완료!
echo.
echo   실행파일 위치: backend\dist\PCFlippingManager.exe
echo   이 파일 하나만 다른 폴더/PC로 복사하면 Python 설치 없이 바로 실행됩니다.
echo   (더블클릭하면 서버가 켜지고 브라우저가 자동으로 열립니다)
echo.
pause
