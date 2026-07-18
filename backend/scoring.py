"""
종합점수 엔진 (PC-Manager의 benchmark_db.json 기반)
- CPU 5,055개 / GPU 2,408개 벤치마크에서 백분위(0~100)를 구하고
- 성능·밸런스·호환성·완성도·가성비를 합산해 0~100 종합점수 + S~D 등급 산출
- 부품별 등급(일반/레어/에픽/전설)도 여기서 계산
"""
import bisect
import json
import os
import re

from compatibility import check_compatibility, _normalize as normalize

_BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(_BASE, "benchmark_db.json"), encoding="utf-8") as f:
    _BENCH = json.load(f)

def _build_keys(entries: list[dict]) -> dict:
    """정규화된 key → score. 'i5 9400f 2 90ghz'처럼 클럭 접미사가 붙은 키는
    접미사를 뗀 버전('i5 9400f')도 함께 등록 (중복 시 높은 점수 유지)"""
    keys: dict[str, float] = {}
    for e in entries:
        key, score = e.get("key"), e.get("score", 0)
        if not key:
            continue
        variants = {key, re.sub(r"(\s+\d+)*\s*[\d.]+\s*[gm]hz$", "", key).strip()}
        for v in variants:
            v = normalize(v)
            if v and (v not in keys or score > keys[v]):
                keys[v] = score
    return keys


_CPU_KEYS = _build_keys(_BENCH.get("cpu", []))
_GPU_KEYS = _build_keys(_BENCH.get("gpu", []))
_CPU_SORTED = sorted(_CPU_KEYS.values())
_GPU_SORTED = sorted(_GPU_KEYS.values())

# 목적별 CPU/GPU 가중치
PURPOSE_WEIGHTS = {
    "gaming": {"cpu": 0.35, "gpu": 0.65},
    "work": {"cpu": 0.65, "gpu": 0.35},
    "streaming": {"cpu": 0.55, "gpu": 0.45},
    "office": {"cpu": 0.70, "gpu": 0.30},
}
PURPOSE_LABELS = {
    "gaming": "게임", "work": "작업", "streaming": "스트리밍", "office": "사무",
}

REQUIRED_SLOTS = ["cpu", "motherboard", "ram", "storage", "psu", "case"]


def _find_bench(name: str, keys: dict) -> float:
    """이름에 포함된 가장 긴 key의 점수 반환 (없으면 0)"""
    name_norm = normalize(name)
    best_key, best_len = None, 0
    for key in keys:
        if key in name_norm and len(key) > best_len:
            best_key, best_len = key, len(key)
    return keys[best_key] if best_key else 0


def _percentile(score: float, sorted_scores: list) -> float:
    """전체 벤치마크 DB에서의 백분위 (0~100)"""
    if score <= 0 or not sorted_scores:
        return 0
    idx = bisect.bisect_left(sorted_scores, score)
    return round(idx / len(sorted_scores) * 100, 1)


# 부품 등급(게임식 레어도) 절대점수 컷 — 벤치 DB에 구형이 많아 백분위 대신 사용
_RARITY_CUTS = {
    "cpu": [(45000, "legendary"), (28000, "epic"), (15000, "rare")],
    "gpu": [(30000, "legendary"), (16000, "epic"), (9000, "rare")],
}


def part_performance(category: str, brand: str, model: str) -> dict:
    """부품 하나의 벤치마크 점수/백분위/등급"""
    name = f"{brand} {model}".strip()
    if category == "cpu":
        score = _find_bench(name, _CPU_KEYS)
        pct = _percentile(score, _CPU_SORTED)
    elif category == "gpu":
        score = _find_bench(name, _GPU_KEYS)
        pct = _percentile(score, _GPU_SORTED)
    else:
        return {"score": 0, "percentile": None, "rarity": "common"}
    rarity = "common"
    for cut, tier in _RARITY_CUTS[category]:
        if score >= cut:
            rarity = tier
            break
    return {"score": score, "percentile": pct, "rarity": rarity}


def grade_of(score: float) -> str:
    if score >= 90:
        return "S"
    if score >= 78:
        return "A"
    if score >= 62:
        return "B"
    if score >= 45:
        return "C"
    return "D"


def score_build(parts: list[dict], purpose: str = "gaming", purchase_cost: float | None = None) -> dict:
    """
    부품 목록(dict: category/brand/model/specs)으로 종합점수 계산.
    purchase_cost가 있으면 가성비 항목 포함.
    """
    cats = {}
    for p in parts:
        cats.setdefault(p["category"], []).append(p)

    # ── 성능 (벤치마크 백분위, 목적별 가중치) ──
    cpu_pct, gpu_pct = 0.0, 0.0
    cpu_bench, gpu_bench = 0, 0
    if "cpu" in cats:
        c = cats["cpu"][0]
        cpu_bench = _find_bench(f"{c['brand']} {c['model']}", _CPU_KEYS)
        cpu_pct = _percentile(cpu_bench, _CPU_SORTED)
    if "gpu" in cats:
        g = cats["gpu"][0]
        gpu_bench = _find_bench(f"{g['brand']} {g['model']}", _GPU_KEYS)
        gpu_pct = _percentile(gpu_bench, _GPU_SORTED)

    w = PURPOSE_WEIGHTS.get(purpose, PURPOSE_WEIGHTS["gaming"])
    if gpu_pct > 0 and cpu_pct > 0:
        performance = cpu_pct * w["cpu"] + gpu_pct * w["gpu"]
    elif cpu_pct > 0:
        performance = cpu_pct * 0.8  # 내장그래픽 가정 페널티
    elif gpu_pct > 0:
        performance = gpu_pct * 0.5
    else:
        performance = 0

    # 목적별 성능 (검사실 레이더용)
    purpose_scores = {}
    for pk, pw in PURPOSE_WEIGHTS.items():
        if gpu_pct > 0 and cpu_pct > 0:
            ps = cpu_pct * pw["cpu"] + gpu_pct * pw["gpu"]
        elif cpu_pct > 0:
            ps = cpu_pct * 0.8
        else:
            ps = gpu_pct * 0.5
        purpose_scores[pk] = round(ps)

    # ── 밸런스 (CPU-GPU 백분위 격차) ──
    bottleneck = None
    if cpu_pct > 0 and gpu_pct > 0:
        gap = abs(cpu_pct - gpu_pct)
        balance = max(0, 100 - gap * 1.5)
        if gap > 25:
            weaker = "CPU" if cpu_pct < gpu_pct else "GPU"
            bottleneck = f"{weaker} 병목 주의 — CPU 백분위 {cpu_pct:.0f} vs GPU 백분위 {gpu_pct:.0f}"
    else:
        balance = 50 if (cpu_pct or gpu_pct) else 0

    # ── 호환성 ──
    compat = check_compatibility(parts)
    compat_score = max(0, 100 - 45 * len(compat["issues"]) - 5 * len(compat["warnings"]))

    # ── 완성도 (필수 슬롯 충족) ──
    have = set(cats.keys())
    if "ssd" in have or "hdd" in have:
        have.add("storage")
    filled = sum(1 for slot in REQUIRED_SLOTS if slot in have)
    completeness = round(filled / len(REQUIRED_SLOTS) * 100)
    missing = [slot for slot in REQUIRED_SLOTS if slot not in have]

    # ── 가성비 (성능 / 투입 비용) — 반쯤 완성된 빌드는 제외 ──
    value = None
    if purchase_cost and purchase_cost > 0 and performance > 0 and completeness >= 50:
        cost_man = purchase_cost / 10000  # 만원 단위
        value = round(min(100, performance / max(cost_man, 1) * 60))

    # ── 종합 ──
    if value is not None:
        overall = performance * 0.30 + balance * 0.15 + compat_score * 0.25 + completeness * 0.15 + value * 0.15
    else:
        overall = performance * 0.35 + balance * 0.15 + compat_score * 0.25 + completeness * 0.25
    overall = round(overall)

    return {
        "overall": overall,
        "grade": grade_of(overall),
        "purpose": purpose,
        "purpose_label": PURPOSE_LABELS.get(purpose, purpose),
        "breakdown": {
            "performance": round(performance),
            "balance": round(balance),
            "compatibility": compat_score,
            "completeness": completeness,
            "value": value,
        },
        "cpu": {"benchmark": cpu_bench, "percentile": cpu_pct},
        "gpu": {"benchmark": gpu_bench, "percentile": gpu_pct},
        "purpose_scores": purpose_scores,
        "bottleneck": bottleneck,
        "missing_slots": missing,
        "compat_issues": compat["issues"],
        "compat_warnings": compat["warnings"],
    }
