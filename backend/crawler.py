"""
시세 크롤러 — 다나와(신품가 기준점) · 번개장터(중고) · 중고나라(중고)

정확도 개선:
- 부품 시세 조회 시 완본체/노트북/세트 매물 제외 (부품 단품 가격만)
- 제목에 모델 번호 토큰이 실제로 포함된 매물만 인정
- 비정상 가격(1만 미만 / 500만 초과) 제외
- 통계는 평균 대신 중앙값 + IQR 이상치 제거 (calculate_pc_value)
"""
import asyncio
import json
import re
import statistics
from urllib.parse import quote

import aiohttp
from bs4 import BeautifulSoup

from compatibility import KOREAN_ALIASES

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ko-KR,ko;q=0.9",
}

# 부품 검색인데 완본체/노트북 매물이 섞이는 걸 거르는 패턴
FULLPC_RE = re.compile(
    r"본체|컴퓨터|노트북|세트|풀\s?셋|데스크탑|데스크톱|조립\s?PC|완본체|게이밍\s?PC|일체형|맥북|아이맥",
    re.IGNORECASE,
)
# 고장/부품용 매물 (정상품 시세를 왜곡)
BROKEN_RE = re.compile(r"고장|불량|파손|부품용|수리용|뻥파워|AS용", re.IGNORECASE)
# "삽니다/구합니다" 같은 매수 글 — 판매 호가가 아니라 사려는 사람이 부르는 값이라
# 파는 사람 시세와는 성격이 달라서 같이 섞으면 왜곡된다.
BUY_REQUEST_RE = re.compile(r"삽니다|구합니다|구매합니다|찾습니다|매입합니다|구입합니다", re.IGNORECASE)

# "본체/세트" 같은 단어 없이도 다른 부품을 같이 얹어 파는 번들 매물이 있다
# (예: CPU를 검색했는데 "라이젠5 5600 + RTX2060 + RAM16GB" 매물) — 이런 건
# 값이 부품 하나 값이 아니라 여러 개를 합친 값이라 시세를 크게 왜곡한다.
# 검색 카테고리와 다른 카테고리의 부품이 같이 언급되면 번들로 보고 제외한다.
_GPU_HINT = r"rtx\s?\d{3,4}|gtx\s?\d{3,4}|\brx\s?\d{3,4}"
_CPU_HINT = r"라이젠|ryzen|인텔\s?i[3579]|intel\s?i[3579]|펜티엄|pentium"
_MEM_STORAGE_HINT = r"ram\s?\d+\s?gb|\d+\s?gb\s?ram|메모리\s?\d+\s?gb|ssd\s?\d{2,4}\s?gb|\d{2,4}\s?gb\s?ssd|hdd\s?\d"
BUNDLE_HINTS = {
    "cpu": re.compile(f"{_GPU_HINT}|{_MEM_STORAGE_HINT}", re.IGNORECASE),
    "gpu": re.compile(f"{_CPU_HINT}|{_MEM_STORAGE_HINT}", re.IGNORECASE),
    "ram": re.compile(f"{_CPU_HINT}|{_GPU_HINT}", re.IGNORECASE),
    "ssd": re.compile(f"{_CPU_HINT}|{_GPU_HINT}", re.IGNORECASE),
    "hdd": re.compile(f"{_CPU_HINT}|{_GPU_HINT}", re.IGNORECASE),
    "motherboard": re.compile(f"{_CPU_HINT}|{_GPU_HINT}", re.IGNORECASE),
}

MIN_PRICE = 10_000
MAX_PRICE = 5_000_000


# 공백으로 붙는 GPU 변형 접미사 — 쿼리에 없는데 매물에 붙어있으면 다른 모델(다른 시세대)로 간주
VARIANT_SUFFIXES = {"ti", "super", "xt", "s"}


def _title_words(s: str) -> list[str]:
    """소문자화 + 한글 별칭 치환 후 단어 단위로 분리 (공백을 없애버리지 않아 '5600'과
    '5600x'를 서로 다른 단어로 구분할 수 있다 — model_tokens/is_relevant가 함께 쓴다)"""
    s = s.lower()
    for ko, en in KOREAN_ALIASES:
        s = s.replace(ko, en)
    s = re.sub(r"[^a-z0-9가-힣]+", " ", s)
    return s.split()


def model_tokens(query: str) -> list[str]:
    """모델 식별력이 있는 토큰(숫자 포함 단어)만 추출. 예: 'GTX 1660 6GB' → ['gtx', '1660']"""
    tokens = []
    for t in _title_words(query):
        if t in ("gb", "tb", "중고"):
            continue
        # 용량 표기(6gb, 500gb)는 식별 토큰에서 제외
        if re.fullmatch(r"\d+(gb|tb|g|t)", t):
            continue
        tokens.append(t)
    return tokens[:4]


def is_relevant(title: str, tokens: list[str]) -> bool:
    """모델 토큰이 제목에 '단어 단위로 정확히' 포함돼 있는지 확인.
    예전엔 공백을 다 지우고 부분일치로 봐서 '5600' 검색에 '5600X'/'5600G' 같은
    완전히 다른(시세도 다른) 모델까지 섞여 들어오는 문제가 있었다 — 단어 경계를
    지키고, Ti/Super/XT처럼 띄어써지는 변형 접미사도 쿼리에 없으면 걸러낸다."""
    title_words = _title_words(title)
    query_words = set(tokens)
    digit_tokens = [tok for tok in tokens if any(c.isdigit() for c in tok)]
    check = digit_tokens or tokens
    if not all(tok in title_words for tok in check):
        return False
    for tok in digit_tokens:
        idx = title_words.index(tok)
        nxt = title_words[idx + 1] if idx + 1 < len(title_words) else None
        if nxt in VARIANT_SUFFIXES and nxt not in query_words:
            return False
    for tok in tokens:
        if tok in VARIANT_SUFFIXES and tok not in title_words:
            return False
    return True


def clean_listings(listings: list[dict], query: str, parts_only: bool = True, category: str = "") -> list[dict]:
    """관련성/완본체/번들/가격 필터"""
    tokens = model_tokens(query)
    bundle_re = BUNDLE_HINTS.get(category) if parts_only else None
    out = []
    for it in listings:
        price = it.get("price", 0)
        if not (MIN_PRICE <= price <= MAX_PRICE):
            continue
        title = it.get("title", "")
        if parts_only and FULLPC_RE.search(title):
            continue
        if parts_only and BROKEN_RE.search(title):
            continue
        if parts_only and BUY_REQUEST_RE.search(title):
            continue
        if bundle_re and bundle_re.search(title):
            continue
        if tokens and not is_relevant(title, tokens):
            continue
        out.append(it)
    return out


async def fetch(session: aiohttp.ClientSession, url: str, **kwargs) -> str | None:
    try:
        async with session.get(url, headers=HEADERS, timeout=aiohttp.ClientTimeout(total=10), **kwargs) as resp:
            if resp.status == 200:
                return await resp.text()
    except Exception:
        pass
    return None


async def search_danawa_direct(query: str, session: aiohttp.ClientSession) -> list[dict]:
    """다나와 최저가 검색 — 신품 가격 기준점 (condition=new)"""
    results = []
    url = f"https://search.danawa.com/dsearch.php?query={quote(query)}&tab=goods"

    html = await fetch(session, url)
    if not html:
        return results

    soup = BeautifulSoup(html, "html.parser")
    for item in soup.select(".prod_main_info")[:8]:
        name_el = item.select_one(".prod_name a")
        price_el = item.select_one(".price_sect strong")
        if not name_el:
            continue
        price = parse_price(price_el.get_text(strip=True) if price_el else "")
        if not price:
            continue
        results.append({
            "source": "danawa",
            "condition": "new",
            "title": name_el.get_text(strip=True),
            "price": price,
            "url": name_el.get("href", ""),
        })

    return results


async def search_bunjang(query: str, session: aiohttp.ClientSession) -> list[dict]:
    """번개장터 API 검색 (중고)"""
    results = []
    url = f"https://api.bunjang.co.kr/api/1/find_v2.json?q={quote(query)}&order=score&n=30&stat=ok"

    try:
        async with session.get(url, headers=HEADERS, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            if resp.status == 200:
                data = await resp.json()
                for item in data.get("list", [])[:30]:
                    price = int(item.get("price", 0) or 0)
                    name = item.get("name", "")
                    pid = item.get("pid", "")
                    if name and price:
                        results.append({
                            "source": "bunjang",
                            "condition": "used",
                            "title": name,
                            "price": price,
                            "url": f"https://m.bunjang.co.kr/products/{pid}",
                        })
    except Exception:
        pass

    return results


async def search_junggo(query: str, session: aiohttp.ClientSession) -> list[dict]:
    """중고나라 검색 API (중고)"""
    results = []
    url = "https://search-api.joongna.com/v3/search/all"
    headers = {**HEADERS, "Content-Type": "application/json", "Origin": "https://web.joongna.com"}
    body = json.dumps({"searchWord": query, "page": 0, "size": 30})

    try:
        async with session.post(url, data=body, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            if resp.status == 200:
                data = await resp.json()
                for item in (data.get("data", {}).get("items") or [])[:30]:
                    price = int(item.get("price", 0) or 0)
                    title = item.get("title", "")
                    seq = item.get("seq", "")
                    if title and price:
                        results.append({
                            "source": "joongna",
                            "condition": "used",
                            "title": title,
                            "price": price,
                            "url": f"https://web.joongna.com/product/{seq}",
                        })
    except Exception:
        pass

    return results


def parse_price(text: str) -> int:
    """가격 문자열에서 숫자 추출"""
    if not text:
        return 0
    nums = re.sub(r"[^\d]", "", text)
    return int(nums) if nums else 0


async def get_part_prices(brand: str, model: str, category: str) -> list[dict]:
    """부품 시세 조회 — 3개 소스 병렬 + 단품 필터 적용 (세션 공유로 연결 재사용)"""
    query = f"{brand} {model}".strip()

    async with aiohttp.ClientSession() as session:
        results_list = await asyncio.gather(
            search_danawa_direct(query, session),
            search_bunjang(query, session),
            search_junggo(query, session),
            return_exceptions=True,
        )

    all_results = []
    for r in results_list:
        if isinstance(r, list):
            all_results.extend(r)

    valid = clean_listings(all_results, query, parts_only=(category != "etc"), category=category)
    # 중고 먼저, 가격 오름차순
    valid.sort(key=lambda x: (x.get("condition") != "used", x.get("price", 0)))
    return valid


def robust_price_stats(prices: list[int]) -> dict | None:
    """중앙값 + IQR 이상치 제거 통계"""
    if not prices:
        return None
    s = sorted(prices)
    if len(s) >= 4:
        q1 = s[len(s) // 4]
        q3 = s[(3 * len(s)) // 4]
        iqr = q3 - q1
        lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        filtered = [p for p in s if lo <= p <= hi] or s
    else:
        filtered = s
    return {
        "median": int(statistics.median(filtered)),
        "min": min(filtered),
        "max": max(filtered),
        "count": len(filtered),
    }


def calculate_pc_value(parts_with_prices: list[dict]) -> dict:
    """PC 전체 중고 가치 계산 — 중고 매물 중앙값 기반"""
    part_values = []
    total_estimate = 0
    total_min = 0
    total_max = 0

    for item in parts_with_prices:
        prices = item.get("prices", [])
        used = [p["price"] for p in prices if p.get("condition") == "used" and p.get("price", 0) > 0]
        new_prices = [p["price"] for p in prices if p.get("condition") == "new" and p.get("price", 0) > 0]

        stats = robust_price_stats(used)
        estimate = stats["median"] if stats else None

        # 다나와 신품가 sanity: 중고 중앙값보다 싼 "신품"은 액세서리/오검색 → 제외
        floor = estimate or MIN_PRICE
        sane_new = [p for p in new_prices if p >= floor]
        new_price = min(sane_new) if sane_new else None
        if estimate:
            total_estimate += estimate
            total_min += stats["min"]
            total_max += stats["max"]

        part_values.append({
            "part": item["part"],
            "estimate": estimate,          # 중고 중앙값 (권장가 기준)
            "n_used": stats["count"] if stats else 0,
            "min_price": stats["min"] if stats else 0,
            "max_price": stats["max"] if stats else 0,
            "new_price": new_price,        # 다나와 신품 최저가 (참고)
            "cached": item.get("cached", False),
        })

    return {
        "parts": part_values,
        "total_estimate": total_estimate,
        "total_min": total_min,
        "total_max": total_max,
    }
