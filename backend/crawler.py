"""
다나와, 당근마켓, 중고나라 중고 시세 크롤러
"""
import asyncio
import aiohttp
import re
from urllib.parse import quote
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ko-KR,ko;q=0.9",
}


async def fetch(session: aiohttp.ClientSession, url: str, **kwargs) -> str | None:
    try:
        async with session.get(url, headers=HEADERS, timeout=aiohttp.ClientTimeout(total=10), **kwargs) as resp:
            if resp.status == 200:
                return await resp.text()
    except Exception:
        pass
    return None


async def search_danawa(query: str) -> list[dict]:
    """다나와 중고장터 검색"""
    results = []
    url = f"https://m.danawa.com/search/?query={quote(query)}&cate=0"

    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        if not html:
            return results

        soup = BeautifulSoup(html, "html.parser")

        # 다나와 상품 카드 파싱
        items = soup.select(".prod_info") or soup.select(".item_product_info")
        for item in items[:5]:
            title_el = item.select_one(".prod_name a") or item.select_one("a")
            price_el = item.select_one(".price_sect strong") or item.select_one(".prc_item")

            if not title_el:
                continue

            title = title_el.get_text(strip=True)
            price_text = price_el.get_text(strip=True) if price_el else ""
            price = parse_price(price_text)

            href = title_el.get("href", "")
            if href and not href.startswith("http"):
                href = "https://m.danawa.com" + href

            if title:
                results.append({
                    "source": "danawa",
                    "title": title,
                    "price": price,
                    "url": href,
                })

    return results


async def search_danawa_direct(query: str) -> list[dict]:
    """다나와 PC 부품 가격 직접 검색"""
    results = []
    url = f"https://search.danawa.com/dsearch.php?query={quote(query)}&tab=goods"

    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        if not html:
            return results

        soup = BeautifulSoup(html, "html.parser")
        items = soup.select(".prod_main_info")

        for item in items[:5]:
            name_el = item.select_one(".prod_name a")
            price_el = item.select_one(".price-sect strong")

            if not name_el:
                continue

            name = name_el.get_text(strip=True)
            price_text = price_el.get_text(strip=True) if price_el else ""
            price = parse_price(price_text)

            href = name_el.get("href", "")
            results.append({
                "source": "danawa",
                "title": name,
                "price": price,
                "url": href,
            })

    return results


async def search_junggo(query: str) -> list[dict]:
    """중고나라 검색 (카페 검색)"""
    results = []
    url = f"https://www.joongna.com/search?keyword={quote(query)}"

    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        if not html:
            return results

        soup = BeautifulSoup(html, "html.parser")

        # 중고나라 상품 리스트
        items = soup.select(".item_list li") or soup.select("[class*='item']")
        for item in items[:5]:
            title_el = item.select_one(".item_title") or item.select_one("a")
            price_el = item.select_one(".item_price") or item.select_one("[class*='price']")

            if not title_el:
                continue

            title = title_el.get_text(strip=True)
            price_text = price_el.get_text(strip=True) if price_el else ""
            price = parse_price(price_text)

            href = title_el.get("href", "") if title_el.name == "a" else ""
            if href and not href.startswith("http"):
                href = "https://www.joongna.com" + href

            if title and price:
                results.append({
                    "source": "joongna",
                    "title": title,
                    "price": price,
                    "url": href,
                })

    return results


async def search_bunjang(query: str) -> list[dict]:
    """번개장터 API 검색"""
    results = []
    url = f"https://api.bunjang.co.kr/api/1/find_v2.json?q={quote(query)}&order=date&n=10&stat=ok"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=HEADERS, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    for item in data.get("list", [])[:5]:
                        price = int(item.get("price", 0))
                        name = item.get("name", "")
                        pid = item.get("pid", "")
                        if name and price:
                            results.append({
                                "source": "bunjang",
                                "title": name,
                                "price": price,
                                "url": f"https://m.bunjang.co.kr/products/{pid}",
                            })
        except Exception:
            pass

    return results


def parse_price(text: str) -> int:
    """가격 문자열에서 숫자 추출"""
    if not text:
        return 0
    nums = re.sub(r"[^\d]", "", text)
    if not nums:
        return 0
    price = int(nums)
    # 원 단위 보정 (ex: 150,000 → 150000)
    return price


async def get_part_prices(brand: str, model: str, category: str) -> list[dict]:
    """부품 종합 시세 조회"""
    query = f"{brand} {model} 중고".strip()

    tasks = [
        search_danawa_direct(f"{brand} {model}"),
        search_bunjang(query),
        search_junggo(query),
    ]

    results_list = await asyncio.gather(*tasks, return_exceptions=True)

    all_results = []
    for r in results_list:
        if isinstance(r, list):
            all_results.extend(r)

    # 가격 있는 것만, 가격순 정렬
    valid = [r for r in all_results if r.get("price", 0) > 0]
    valid.sort(key=lambda x: x["price"])

    return valid


def calculate_pc_value(parts_with_prices: list[dict]) -> dict:
    """PC 전체 중고 가치 계산"""
    total_min = 0
    total_max = 0
    part_values = []

    for item in parts_with_prices:
        prices = [p["price"] for p in item.get("prices", []) if p.get("price", 0) > 0]
        if prices:
            min_price = min(prices)
            max_price = max(prices)
            avg_price = int(sum(prices) / len(prices))
            total_min += min_price
            total_max += max_price
        else:
            min_price = max_price = avg_price = 0

        part_values.append({
            "part": item["part"],
            "min_price": min_price,
            "max_price": max_price,
            "avg_price": avg_price,
        })

    return {
        "parts": part_values,
        "total_min": total_min,
        "total_max": total_max,
        "total_avg": int((total_min + total_max) / 2) if (total_min + total_max) > 0 else 0,
    }
