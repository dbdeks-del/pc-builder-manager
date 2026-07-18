# 부품 카탈로그(parts_db.json) 최대 커버리지 빌드 스크립트
#
# 소스 3개를 병합해서 중고 시장(10년+ 구형 포함)을 최대한 커버:
#   1. GitHub docyx/pc-part-dataset (PCPartPicker 스크랩, 최신 전체본)
#   2. benchmark_db.json — PassMark 계열 CPU 5,055개 / GPU 2,408개
#      (GTX 750 Ti, HD 7970, i7-4790K, FX-8350 같은 구형이 여기에 다 있음)
#   3. 기존 parts_db.json — PCPartPicker에서 내려간(delisted) 항목 보존
# + 구형 메인보드 큐레이션 목록 (AM3+/FM2+/H61 등 국내 중고시장 단골)
#
# 사용법: python build_parts_db.py            (인터넷 필요)
#        python build_parts_db.py --offline  (docyx 생략, 로컬 소스만 병합)
import json
import os
import re
import sys
import urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "parts_db.json")
DOCYX = "https://raw.githubusercontent.com/docyx/pc-part-dataset/main/data/json/"


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9가-힣]", "", s.lower())


# ── 1. docyx 변환 (원본 build_db.py 로직) ──────────────────────

def spec_cpu(o):
    p = []
    if o.get("core_count"): p.append(f"{o['core_count']}코어")
    if o.get("boost_clock"): p.append(f"{o['boost_clock']}GHz")
    if o.get("tdp"): p.append(f"{o['tdp']}W")
    return " · ".join(p)

def spec_gpu(o):
    p = []
    if o.get("chipset"): p.append(o["chipset"])
    if o.get("memory"): p.append(f"{o['memory']}GB")
    return " · ".join(p)

def spec_board(o):
    p = []
    if o.get("socket"): p.append(o["socket"])
    if o.get("form_factor"): p.append(o["form_factor"])
    if o.get("memory_type"): p.append(o["memory_type"])
    return " · ".join(p)

def spec_mem(o):
    p = []
    if o.get("speed"): p.append("-".join(str(x) for x in o["speed"]) if isinstance(o["speed"], list) else str(o["speed"]))
    if o.get("modules"): p.append("x".join(str(x) for x in o["modules"]) if isinstance(o["modules"], list) else str(o["modules"]))
    return " · ".join(p)

def spec_storage(o):
    p = []
    if o.get("capacity"): p.append(f"{o['capacity']}GB")
    if o.get("type"): p.append(str(o["type"]))
    if o.get("form_factor"): p.append(str(o["form_factor"]))
    return " · ".join(p)

def spec_psu(o):
    p = []
    if o.get("wattage"): p.append(f"{o['wattage']}W")
    if o.get("efficiency"): p.append(str(o["efficiency"]))
    if o.get("modular"): p.append(str(o["modular"]))
    return " · ".join(p)

SOURCES = [
    ("cpu.json", "CPU", spec_cpu),
    ("video-card.json", "그래픽카드", spec_gpu),
    ("motherboard.json", "메인보드", spec_board),
    ("memory.json", "RAM", spec_mem),
    ("internal-hard-drive.json", "저장장치", spec_storage),
    ("power-supply.json", "파워", spec_psu),
    ("case.json", "케이스", lambda o: str(o.get("type", "") or "")),
    ("cpu-cooler.json", "쿨러", lambda o: ""),
]


def fetch_docyx() -> dict:
    db = {}
    for fname, cat, specfn in SOURCES:
        try:
            with urllib.request.urlopen(DOCYX + fname, timeout=90) as r:
                arr = json.loads(r.read().decode("utf-8"))
        except Exception as e:
            print(f"  ! {fname} 다운로드 실패: {e} — 이 카테고리는 로컬 소스만 사용")
            db[cat] = []
            continue
        items, seen = [], set()
        for o in arr:
            nm = (o.get("name") or "").strip()
            if not nm or nm in seen:
                continue
            seen.add(nm)
            items.append({"n": nm, "s": specfn(o)})
        db[cat] = items
        print(f"  docyx {cat:6s} {len(arr):5d} → {len(items):5d}개")
    return db


# ── 2. 벤치마크 DB → 카탈로그 항목 ─────────────────────────────

def bench_entries() -> tuple[list, list]:
    with open(os.path.join(BASE, "benchmark_db.json"), encoding="utf-8") as f:
        bench = json.load(f)
    cpus, gpus = [], []
    for e in bench.get("cpu", []):
        name = re.sub(r"\s*@.*$", "", e.get("name", "")).strip()
        if name:
            cpus.append({"n": name, "s": f"벤치 {e.get('score', 0):,}"})
    for e in bench.get("gpu", []):
        name = (e.get("name") or "").strip()
        if name:
            gpus.append({"n": name, "s": f"벤치 {e.get('score', 0):,}"})
    return cpus, gpus


# ── 3. 구형 메인보드 큐레이션 (국내 중고시장 단골 모델) ─────────

OLD_BOARDS = [
    # AM3+ (FX)
    ("Asus M5A78L-M LX3", "AM3+ · Micro ATX · DDR3"),
    ("Asus M5A97 R2.0", "AM3+ · ATX · DDR3"),
    ("Asus M5A99X EVO R2.0", "AM3+ · ATX · DDR3"),
    ("Gigabyte GA-970A-DS3P", "AM3+ · ATX · DDR3"),
    ("Gigabyte GA-990FXA-UD3", "AM3+ · ATX · DDR3"),
    ("MSI 970 Gaming", "AM3+ · ATX · DDR3"),
    ("MSI 970A-G43", "AM3+ · ATX · DDR3"),
    ("ASRock 970 Extreme4", "AM3+ · ATX · DDR3"),
    ("ASRock 990FX Extreme4", "AM3+ · ATX · DDR3"),
    # FM2/FM2+ (APU)
    ("Asus A88XM-A", "FM2+ · Micro ATX · DDR3"),
    ("Gigabyte GA-F2A88XM-D3H", "FM2+ · Micro ATX · DDR3"),
    ("MSI A88XM-E45", "FM2+ · Micro ATX · DDR3"),
    ("ASRock FM2A88X Extreme4+", "FM2+ · ATX · DDR3"),
    # LGA1155 (2nd/3rd gen)
    ("Asus P8H61-M LE", "LGA1155 · Micro ATX · DDR3"),
    ("Asus P8Z77-V LX", "LGA1155 · ATX · DDR3"),
    ("Gigabyte GA-H61M-DS2", "LGA1155 · Micro ATX · DDR3"),
    ("Gigabyte GA-B75M-D3H", "LGA1155 · Micro ATX · DDR3"),
    ("Gigabyte GA-Z77-DS3H", "LGA1155 · ATX · DDR3"),
    ("MSI H61M-P31", "LGA1155 · Micro ATX · DDR3"),
    ("MSI B75MA-P45", "LGA1155 · Micro ATX · DDR3"),
    ("ASRock H61M-VS", "LGA1155 · Micro ATX · DDR3"),
    ("ASRock B75M R2.0", "LGA1155 · Micro ATX · DDR3"),
    ("ASRock Z77 Extreme4", "LGA1155 · ATX · DDR3"),
    # LGA1156 (1st gen)
    ("Asus P7P55D-E", "LGA1156 · ATX · DDR3"),
    ("Gigabyte GA-P55A-UD3", "LGA1156 · ATX · DDR3"),
    # LGA775
    ("Asus P5G41T-M LX", "LGA775 · Micro ATX · DDR3"),
    ("Gigabyte GA-G41MT-S2", "LGA775 · Micro ATX · DDR3"),
    # AM3 (Phenom II)
    ("Asus M4A785TD-V EVO", "AM3 · ATX · DDR3"),
    ("Gigabyte GA-870A-UD3", "AM3 · ATX · DDR3"),
]


# ── 병합 ───────────────────────────────────────────────────────

def merge(base: dict, extra_items: list, cat: str, added_from: str, counter: dict):
    existing = {norm(e["n"]) for e in base.setdefault(cat, [])}
    n = 0
    for item in extra_items:
        key = norm(item["n"])
        if key and key not in existing:
            base[cat].append(item)
            existing.add(key)
            n += 1
    if n:
        counter[f"{cat} ← {added_from}"] = n


def main():
    offline = "--offline" in sys.argv

    # 기존 DB (delisted 항목 보존용)
    old_db = {}
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as f:
            old_db = json.load(f)

    if offline:
        db = {cat: list(items) for cat, items in old_db.items()}
        print("오프라인 모드: 기존 parts_db.json 기반으로 병합")
    else:
        print("docyx/pc-part-dataset 다운로드 중...")
        db = fetch_docyx()

    counter = {}

    # 기존 DB에만 있던 항목 되살리기 (PCPartPicker에서 내려간 구형)
    for cat, items in old_db.items():
        merge(db, items, cat, "기존 DB 보존", counter)

    # 벤치마크 DB의 CPU/GPU (구형 커버리지의 핵심)
    cpus, gpus = bench_entries()
    merge(db, cpus, "CPU", "벤치마크 DB", counter)
    merge(db, gpus, "그래픽카드", "벤치마크 DB", counter)

    # 구형 보드 큐레이션
    merge(db, [{"n": n_, "s": s_} for n_, s_ in OLD_BOARDS], "메인보드", "큐레이션", counter)

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, separators=(",", ":"))

    print()
    for k, v in counter.items():
        print(f"  +{v:5d}  {k}")
    total = sum(len(v) for v in db.values())
    print(f"\n총 {total:,}개 항목 → {OUT} ({os.path.getsize(OUT) // 1024}KB)")
    for cat, items in db.items():
        print(f"  {cat}: {len(items):,}")


if __name__ == "__main__":
    main()
