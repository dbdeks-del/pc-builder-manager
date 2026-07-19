# -*- mode: python ; coding: utf-8 -*-
# PyInstaller 빌드 스펙 — 단일 실행파일(.exe) 생성
# 사용법: pyinstaller pc_flipping_manager.spec  (backend/ 폴더에서 실행)
from PyInstaller.utils.hooks import collect_all

datas = [
    ("parts_db.json", "."),
    ("benchmark_db.json", "."),
    ("../frontend/index.html", "frontend"),
]
binaries = []
hiddenimports = []

# uvicorn/pydantic/aiohttp은 importlib로 백엔드를 동적 선택하는 부분이 있어서
# PyInstaller 정적 분석이 놓치기 쉽다 — collect_all로 안전하게 전부 포함시킨다.
for pkg in ("uvicorn", "pydantic", "aiohttp"):
    d, b, h = collect_all(pkg)
    datas += d
    binaries += b
    hiddenimports += h

a = Analysis(
    ["launcher.py"],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="PCFlippingManager",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
)
