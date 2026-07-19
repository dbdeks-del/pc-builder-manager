"""
부품 카탈로그 DB (PC-Manager에서 이식한 parts_db.json, 23,512개)
- 한글 카테고리 → 영문 enum 매핑
- 스펙 요약 문자열(s)을 구조화된 specs로 파싱 (호환성 검사에 사용)
"""
import json
import os
import re

_BASE = os.path.dirname(os.path.abspath(__file__))

KO2EN = {
    "CPU": "cpu",
    "그래픽카드": "gpu",
    "메인보드": "motherboard",
    "RAM": "ram",
    "저장장치": "ssd",  # s에 HDD 표기가 있으면 hdd로 재분류
    "파워": "psu",
    "케이스": "case",
    "쿨러": "cooler",
    "기타": "etc",
}

def _parse_specs(category: str, name: str, s: str) -> dict:
    """스펙 요약 문자열을 카테고리별 구조화 specs로 변환"""
    specs = {"summary": s}
    if s.startswith("벤치"):  # 벤치마크 DB 유래 항목은 점수 요약뿐이라 파싱 불가
        return specs
    parts = [p.strip() for p in s.split("·")]

    if category == "cpu":
        # 예: "8코어 · 5.2GHz · 120W"
        for p in parts:
            if m := re.match(r"(\d+)코어", p):
                specs["cores"] = int(m.group(1))
            elif m := re.match(r"([\d.]+)GHz", p):
                specs["boost_clock_ghz"] = float(m.group(1))
            elif m := re.match(r"(\d+)W", p):
                specs["tdp_w"] = int(m.group(1))
    elif category == "gpu":
        # 예: "GeForce RTX 3060 12GB · 12GB"
        if parts:
            specs["chipset"] = re.sub(r"\s*\d+GB$", "", parts[0]).strip()
        for p in parts[1:]:
            if m := re.match(r"(\d+)GB", p):
                specs["vram_gb"] = int(m.group(1))
    elif category == "motherboard":
        # 예: "AM5 · ATX" 또는 "AM3+ · ATX · DDR3"
        if len(parts) >= 1 and parts[0]:
            specs["socket"] = parts[0]
        if len(parts) >= 2 and parts[1]:
            specs["form_factor"] = parts[1]
        for p in parts[2:]:
            if p.upper().startswith("DDR"):
                specs["ddr_type"] = p.upper()
    elif category == "ram":
        # 예: "5-6000 · 2x16"  (DDR세대-속도 · 모듈x용량)
        if parts and (m := re.match(r"(\d)-(\d+)", parts[0])):
            specs["ddr_type"] = f"DDR{m.group(1)}"
            specs["speed_mhz"] = int(m.group(2))
        if len(parts) >= 2 and (m := re.match(r"(\d+)x(\d+)", parts[1])):
            specs["modules"] = int(m.group(1))
            specs["capacity_gb"] = int(m.group(1)) * int(m.group(2))
    elif category in ("ssd", "hdd"):
        # 예: "2000GB · SSD · M.2-2280"
        for p in parts:
            if m := re.match(r"([\d.]+)\s*(GB|TB)", p, re.I):
                cap = float(m.group(1))
                specs["capacity_gb"] = int(cap * 1000) if m.group(2).upper() == "TB" else int(cap)
            elif p.upper() in ("SSD", "HDD"):
                specs["storage_type"] = p.upper()
            elif p:
                specs["form_factor"] = p
    elif category == "psu":
        # 예: "750W · gold · Full"
        for p in parts:
            if m := re.match(r"(\d+)\s*W", p, re.I):
                specs["wattage"] = int(m.group(1))
            elif p.lower() in ("bronze", "silver", "gold", "platinum", "titanium", "plus"):
                specs["efficiency"] = p.capitalize()

    return specs


def _split_brand(name: str) -> tuple[str, str]:
    """이름 첫 단어를 브랜드로 분리"""
    tokens = name.split(None, 1)
    if len(tokens) == 2:
        return tokens[0], tokens[1]
    return "", name


def _load() -> list[dict]:
    path = os.path.join(_BASE, "parts_db.json")
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)

    db = []
    for ko_cat, items in raw.items():
        base_cat = KO2EN.get(ko_cat, "etc")
        for item in items:
            name = item.get("n", "")
            s = item.get("s", "")
            cat = base_cat
            if ko_cat == "저장장치" and "HDD" in s.upper():
                cat = "hdd"
            brand, model = _split_brand(name)
            db.append({
                "category": cat,
                "brand": brand,
                "model": model,
                "name": name,
                "specs": _parse_specs(cat, name, s),
            })
    return db


PARTS_DATABASE = _load()


def search_parts(query: str = "", category: str = "") -> list[dict]:
    query = query.lower().strip()
    results = PARTS_DATABASE

    if category:
        if category in ("ssd", "hdd"):
            results = [p for p in results if p["category"] in ("ssd", "hdd")]
        else:
            results = [p for p in results if p["category"] == category]

    if query:
        tokens = query.split()

        def matches(p):
            text = f"{p['name']} {p['specs'].get('summary', '')}".lower()
            return all(t in text for t in tokens)

        results = [p for p in results if matches(p)]

    return results[:30]
