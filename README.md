# PC Builder Manager

PC 부품 호환성 체크 및 견적 관리 도구입니다.

## 다른 PC에서 받아서 실행하기

1. **Python 3.10 이상 설치** — https://www.python.org/downloads/
   설치할 때 **"Add Python to PATH"** 체크 필수.

2. 이 저장소를 다운로드/클론:
   ```
   git clone https://github.com/dbdeks-del/pc-builder-manager.git
   ```

3. `start.bat` **더블클릭**.
   - 첫 실행 시 필요한 라이브러리를 자동 설치합니다(인터넷 필요).
   - backend 서버(http://localhost:8000)가 켜지고 브라우저가 자동으로 열립니다.

4. 종료하려면 실행 창에서 아무 키나 누르세요.

## 구조

- `backend/` — FastAPI 서버 (부품 DB, 호환성 검사, 크롤러)
- `frontend/` — 웹 UI (index.html)
- `start.bat` — 원클릭 실행 스크립트
