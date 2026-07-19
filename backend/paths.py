"""
개발 환경과 PyInstaller 번들(.exe) 모두에서 동작하는 경로 헬퍼.
PyInstaller onefile로 묶이면 실행 시 임시 폴더(sys._MEIPASS)에 데이터가 풀리므로,
'현재 파일 옆'이라는 가정이 깨진다 — 이 모듈이 그 차이를 감춘다.
"""
import os
import sys

_FROZEN = hasattr(sys, "_MEIPASS")
BASE_DIR = sys._MEIPASS if _FROZEN else os.path.dirname(os.path.abspath(__file__))


def resource_path(*parts: str) -> str:
    """backend/ 데이터 파일(parts_db.json, benchmark_db.json 등) 경로.
    개발 환경도 번들도 이 폴더 바로 아래에 위치하도록 배치한다."""
    return os.path.join(BASE_DIR, *parts)


def frontend_path() -> str:
    """frontend/index.html 경로 — 번들에서는 BASE_DIR/frontend/, 개발에서는 backend/../frontend/"""
    if _FROZEN:
        return os.path.join(BASE_DIR, "frontend", "index.html")
    return os.path.join(BASE_DIR, "..", "frontend", "index.html")


def data_dir() -> str:
    """DB 파일처럼 실행할 때마다 남아있어야 하는 데이터를 저장할 폴더.
    resource_path()의 BASE_DIR(_MEIPASS)는 exe를 새로 켤 때마다 다시 풀리는 임시
    폴더라 여기 쓰면 데이터가 매번 사라진다 — .exe 파일 옆(또는 backend/) 폴더를 쓴다."""
    if _FROZEN:
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))
