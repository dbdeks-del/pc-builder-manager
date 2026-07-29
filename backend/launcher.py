"""
PC 플리핑 매니저 실행 진입점 — python launcher.py 로 직접 실행하거나
PyInstaller로 묶어 하나의 실행파일(.exe)로 배포할 때 이 파일을 엔트리포인트로 쓴다.
서버를 띄우고 잠시 후 기본 브라우저로 자동으로 연다.
0.0.0.0으로 바인딩하므로 같은 와이파이(인터넷 연결 없어도 됨)에 있는 휴대폰에서도
이 PC의 로컬 IP로 접속할 수 있다.
"""
import os
import socket
import threading
import time
import webbrowser

import uvicorn

PORT = 8000


def lan_ip() -> str | None:
    """이 PC의 로컬 네트워크 IP (인터넷 연결 여부와 무관 — 실제 패킷은 안 나감)"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("192.168.0.1", 1))  # 아무 사설 IP나 — 라우팅 테이블 조회용
        return s.getsockname()[0]
    except OSError:
        return None
    finally:
        s.close()


def open_browser():
    time.sleep(1.2)
    webbrowser.open(f"http://127.0.0.1:{PORT}")


def main():
    ip = lan_ip()
    print("=" * 44)
    print("  PC 플리핑 매니저 실행 중")
    print(f"  이 PC에서: http://127.0.0.1:{PORT}")
    if ip:
        print(f"  휴대폰/다른 기기에서 (같은 와이파이): http://{ip}:{PORT}")
        print("  ※ 인터넷 연결 없이 같은 와이파이/핫스팟에만 있으면 됩니다")
        print("  ※ 처음 실행 시 Windows 방화벽 허용 창이 뜨면 '허용'을 눌러주세요")
    print("  종료하려면 이 창을 닫으세요 (Ctrl+C)")
    print("=" * 44)

    if not os.environ.get("PCFM_NO_BROWSER"):
        threading.Thread(target=open_browser, daemon=True).start()

    from main import app  # 지연 임포트: 배너를 먼저 찍고 무거운 초기화(부품 DB 로딩 등) 진행
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="warning")


if __name__ == "__main__":
    main()
