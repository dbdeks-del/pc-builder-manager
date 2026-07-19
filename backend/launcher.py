"""
PC 플리핑 매니저 실행 진입점 — python launcher.py 로 직접 실행하거나
PyInstaller로 묶어 하나의 실행파일(.exe)로 배포할 때 이 파일을 엔트리포인트로 쓴다.
서버를 띄우고 잠시 후 기본 브라우저로 자동으로 연다.
"""
import os
import threading
import time
import webbrowser

import uvicorn

PORT = 8000


def open_browser():
    time.sleep(1.2)
    webbrowser.open(f"http://127.0.0.1:{PORT}")


def main():
    print("=" * 44)
    print("  PC 플리핑 매니저 실행 중")
    print(f"  브라우저 주소: http://127.0.0.1:{PORT}")
    print("  종료하려면 이 창을 닫으세요 (Ctrl+C)")
    print("=" * 44)

    if not os.environ.get("PCFM_NO_BROWSER"):
        threading.Thread(target=open_browser, daemon=True).start()

    from main import app  # 지연 임포트: 배너를 먼저 찍고 무거운 초기화(부품 DB 로딩 등) 진행
    uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="warning")


if __name__ == "__main__":
    main()
