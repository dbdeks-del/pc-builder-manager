import json
import sqlite3
from datetime import datetime, timedelta
from typing import Optional
import asyncio

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from database import init_db, get_db, insert, update, delete, get_one, row_dict, now
from compatibility import check_compatibility, analyze_bottleneck, recommend_build
from crawler import get_part_prices, calculate_pc_value
from parts_db import search_parts
from paths import frontend_path
from scoring import score_build, part_performance

app = FastAPI(title="PC Builder Manager", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/", include_in_schema=False)
def frontend_index():
    """프론트엔드를 백엔드가 직접 서빙 — 창을 두 개 띄울 필요 없이 한 프로세스로 동작"""
    return FileResponse(frontend_path())


# ── Pydantic Schemas ──────────────────────────────────────────

class PartCreate(BaseModel):
    category: str
    brand: str = ""
    model: str
    specs: dict = {}
    condition: str = "used"
    owned: bool = True
    purchase_price: Optional[float] = None
    market_price: Optional[float] = None
    pc_id: Optional[int] = None


class PartUpdate(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    specs: Optional[dict] = None
    condition: Optional[str] = None
    owned: Optional[bool] = None
    purchase_price: Optional[float] = None
    market_price: Optional[float] = None


class PCCreate(BaseModel):
    name: str = "새 PC"


class PCUpdate(BaseModel):
    name: Optional[str] = None


class SellRequest(BaseModel):
    price: float


class WholeIntakePart(BaseModel):
    category: str
    brand: str = ""
    model: str
    specs: dict = {}


class WholeIntake(BaseModel):
    name: str
    purchase_price: float
    parts: list[WholeIntakePart] = []


class LedgerCreate(BaseModel):
    type: str  # buy, sell
    item: str
    price: float
    date: Optional[datetime] = None


# ── Helpers ───────────────────────────────────────────────────

def get_or_404(db: sqlite3.Connection, table: str, obj_id: int, not_found: str) -> sqlite3.Row:
    obj = get_one(db, table, obj_id)
    if not obj:
        raise HTTPException(404, not_found)
    return obj


def _owned_or_pc_parts(db: sqlite3.Connection, pc_id: Optional[int]) -> list[dict]:
    """pc_id가 있으면 그 PC에 장착된 부품, 없으면 보유 중인 부품 전체"""
    if pc_id is not None:
        rows = db.execute("SELECT * FROM parts WHERE pc_id = ?", (pc_id,)).fetchall()
    else:
        rows = db.execute("SELECT * FROM parts WHERE owned = 1").fetchall()
    return [row_dict(r) for r in rows]


def part_dict(p: dict) -> dict:
    perf = part_performance(p["category"], p["brand"] or "", p["model"] or "", p["specs"] or {})
    return {
        "id": p["id"], "category": p["category"], "brand": p["brand"], "model": p["model"],
        "specs": p["specs"] or {}, "condition": p["condition"], "owned": p["owned"],
        "purchase_price": p["purchase_price"], "market_price": p["market_price"],
        "pc_id": p["pc_id"], "rarity": perf["rarity"], "percentile": perf["percentile"],
    }


def parts_data_of(parts: list[dict]) -> list[dict]:
    return [{"category": p["category"], "brand": p["brand"] or "", "model": p["model"] or "", "specs": p["specs"] or {}} for p in parts]


def pc_dict(pc: dict, db: sqlite3.Connection, purpose: str = "gaming") -> dict:
    parts = [row_dict(r) for r in db.execute("SELECT * FROM parts WHERE pc_id = ?", (pc["id"],)).fetchall()]
    cost = pc["purchase_price"] if pc["whole"] and pc["purchase_price"] else sum(p["purchase_price"] or 0 for p in parts)
    score = score_build(parts_data_of(parts), purpose, cost or None)
    return {
        "id": pc["id"], "name": pc["name"], "status": pc["status"], "whole": pc["whole"],
        "purchase_price": pc["purchase_price"], "sold_price": pc["sold_price"],
        "created_at": pc["created_at"], "completed_at": pc["completed_at"], "sold_at": pc["sold_at"],
        "parts": [part_dict(p) for p in parts],
        "cost": cost,
        "score": score,
    }


# ── Parts CRUD ────────────────────────────────────────────────

@app.get("/parts")
def list_parts(owned: Optional[bool] = None, in_warehouse: Optional[bool] = None, db: sqlite3.Connection = Depends(get_db)):
    sql = "SELECT * FROM parts WHERE 1=1"
    params: list = []
    if owned is not None:
        sql += " AND owned = ?"
        params.append(int(owned))
    if in_warehouse:
        sql += " AND pc_id IS NULL"
    sql += " ORDER BY id DESC"
    rows = db.execute(sql, params).fetchall()
    return [part_dict(row_dict(r)) for r in rows]


@app.post("/parts")
def create_part(data: PartCreate, db: sqlite3.Connection = Depends(get_db)):
    fields = data.model_dump()
    fields["specs"] = json.dumps(fields["specs"])
    ts = now()
    fields["created_at"] = ts
    fields["updated_at"] = ts
    new_id = insert(db, "parts", **fields)
    return part_dict(row_dict(get_one(db, "parts", new_id)))


@app.put("/parts/{part_id}")
def update_part(part_id: int, data: PartUpdate, db: sqlite3.Connection = Depends(get_db)):
    get_or_404(db, "parts", part_id, "Part not found")
    fields = data.model_dump(exclude_none=True)
    if "specs" in fields:
        fields["specs"] = json.dumps(fields["specs"])
    fields["updated_at"] = now()
    update(db, "parts", part_id, **fields)
    return part_dict(row_dict(get_one(db, "parts", part_id)))


@app.delete("/parts/{part_id}")
def delete_part(part_id: int, db: sqlite3.Connection = Depends(get_db)):
    get_or_404(db, "parts", part_id, "Part not found")
    delete(db, "parts", part_id)
    return {"ok": True}


@app.post("/parts/{part_id}/sell")
def sell_part(part_id: int, data: SellRequest, db: sqlite3.Connection = Depends(get_db)):
    """부품 개별 판매: 장부에 기록하고 인벤토리에서 제거"""
    part = row_dict(get_or_404(db, "parts", part_id, "Part not found"))
    if part["pc_id"] is not None:
        raise HTTPException(400, "PC에 장착된 부품입니다. 먼저 탈착하세요.")
    name = f"{part['brand'] or ''} {part['model'] or ''}".strip()
    margin = data.price - (part["purchase_price"] or 0)
    insert(db, "ledger", type="sell", item=f"[부품판매] {name}", price=data.price, date=now())
    delete(db, "parts", part_id)
    return {"ok": True, "margin": margin}


# ── PC 조립 (조립실) ──────────────────────────────────────────

@app.get("/pcs")
def list_pcs(status: Optional[str] = None, purpose: str = "gaming", db: sqlite3.Connection = Depends(get_db)):
    sql = "SELECT * FROM pcs"
    params: list = []
    if status:
        sql += " WHERE status = ?"
        params.append(status)
    sql += " ORDER BY id DESC"
    rows = db.execute(sql, params).fetchall()
    return [pc_dict(row_dict(r), db, purpose) for r in rows]


@app.post("/pcs")
def create_pc(data: PCCreate, db: sqlite3.Connection = Depends(get_db)):
    new_id = insert(db, "pcs", name=data.name, status="building", whole=0, created_at=now())
    return pc_dict(row_dict(get_one(db, "pcs", new_id)), db)


@app.get("/pcs/{pc_id}")
def get_pc(pc_id: int, purpose: str = "gaming", db: sqlite3.Connection = Depends(get_db)):
    pc = row_dict(get_or_404(db, "pcs", pc_id, "PC not found"))
    return pc_dict(pc, db, purpose)


@app.put("/pcs/{pc_id}")
def update_pc(pc_id: int, data: PCUpdate, db: sqlite3.Connection = Depends(get_db)):
    get_or_404(db, "pcs", pc_id, "PC not found")
    update(db, "pcs", pc_id, **data.model_dump(exclude_none=True))
    return pc_dict(row_dict(get_one(db, "pcs", pc_id)), db)


@app.post("/pcs/{pc_id}/parts/{part_id}")
def attach_part(pc_id: int, part_id: int, db: sqlite3.Connection = Depends(get_db)):
    pc = get_one(db, "pcs", pc_id)
    part = row_dict(get_one(db, "parts", part_id))
    if not pc or not part:
        raise HTTPException(404, "PC or Part not found")
    if part["pc_id"] is not None and part["pc_id"] != pc_id:
        raise HTTPException(400, "이미 다른 PC에 장착된 부품입니다.")
    update(db, "parts", part_id, pc_id=pc_id)
    return pc_dict(row_dict(pc), db)


@app.delete("/pcs/{pc_id}/parts/{part_id}")
def detach_part(pc_id: int, part_id: int, db: sqlite3.Connection = Depends(get_db)):
    part = db.execute("SELECT * FROM parts WHERE id = ? AND pc_id = ?", (part_id, pc_id)).fetchone()
    if not part:
        raise HTTPException(404, "Part not found on this PC")
    update(db, "parts", part_id, pc_id=None)
    pc = get_one(db, "pcs", pc_id)
    return pc_dict(row_dict(pc), db)


@app.post("/pcs/{pc_id}/complete")
def complete_pc(pc_id: int, db: sqlite3.Connection = Depends(get_db)):
    get_or_404(db, "pcs", pc_id, "PC not found")
    update(db, "pcs", pc_id, status="done", completed_at=now())
    return pc_dict(row_dict(get_one(db, "pcs", pc_id)), db)


@app.post("/pcs/{pc_id}/reopen")
def reopen_pc(pc_id: int, db: sqlite3.Connection = Depends(get_db)):
    get_or_404(db, "pcs", pc_id, "PC not found")
    update(db, "pcs", pc_id, status="building", completed_at=None)
    return pc_dict(row_dict(get_one(db, "pcs", pc_id)), db)


@app.post("/pcs/{pc_id}/sell")
def sell_pc(pc_id: int, data: SellRequest, db: sqlite3.Connection = Depends(get_db)):
    pc = row_dict(get_or_404(db, "pcs", pc_id, "PC not found"))
    update(db, "pcs", pc_id, status="sold", sold_price=data.price, sold_at=now())
    insert(db, "ledger", type="sell", item=pc["name"], price=data.price, pc_id=pc_id, date=now())
    return pc_dict(row_dict(get_one(db, "pcs", pc_id)), db)


@app.post("/pcs/{pc_id}/dismantle")
def dismantle_pc(pc_id: int, db: sqlite3.Connection = Depends(get_db)):
    """해체: 부품은 창고로 복귀, PC 카드는 삭제 (장부 기록은 유지)"""
    get_or_404(db, "pcs", pc_id, "PC not found")
    db.execute("UPDATE parts SET pc_id = NULL WHERE pc_id = ?", (pc_id,))
    db.commit()
    delete(db, "pcs", pc_id)
    return {"ok": True}


@app.delete("/pcs/{pc_id}")
def delete_pc(pc_id: int, db: sqlite3.Connection = Depends(get_db)):
    """삭제: 부품까지 함께 삭제"""
    get_or_404(db, "pcs", pc_id, "PC not found")
    db.execute("DELETE FROM parts WHERE pc_id = ?", (pc_id,))
    db.commit()
    delete(db, "pcs", pc_id)
    return {"ok": True}


@app.post("/pcs/whole")
def whole_intake(data: WholeIntake, db: sqlite3.Connection = Depends(get_db)):
    """본체 통째 매입: 완성 PC + 부품들 + 구매 장부를 한 번에 생성"""
    ts = now()
    pc_id = insert(db, "pcs", name=data.name, status="done", whole=1,
                   purchase_price=data.purchase_price, created_at=ts, completed_at=ts)
    for wp in data.parts:
        insert(db, "parts", category=wp.category, brand=wp.brand, model=wp.model,
               specs=json.dumps(wp.specs), pc_id=pc_id, created_at=ts, updated_at=ts)
    insert(db, "ledger", type="buy", item=f"[통매입] {data.name}", price=data.purchase_price, pc_id=pc_id, date=ts)
    return pc_dict(row_dict(get_one(db, "pcs", pc_id)), db)


# ── 종합점수 (검사실) ─────────────────────────────────────────

@app.get("/pcs/{pc_id}/score")
def pc_score(pc_id: int, purpose: str = "gaming", db: sqlite3.Connection = Depends(get_db)):
    pc = row_dict(get_or_404(db, "pcs", pc_id, "PC not found"))
    parts = [row_dict(r) for r in db.execute("SELECT * FROM parts WHERE pc_id = ?", (pc_id,)).fetchall()]
    cost = pc["purchase_price"] if pc["whole"] and pc["purchase_price"] else sum(p["purchase_price"] or 0 for p in parts)
    return score_build(parts_data_of(parts), purpose, cost or None)


# ── 장부 ──────────────────────────────────────────────────────

@app.get("/ledger")
def list_ledger(db: sqlite3.Connection = Depends(get_db)):
    entries = [row_dict(r) for r in db.execute("SELECT * FROM ledger ORDER BY date DESC, id DESC").fetchall()]
    buy_total = sum(e["price"] or 0 for e in entries if e["type"] == "buy")
    sell_total = sum(e["price"] or 0 for e in entries if e["type"] == "sell")
    return {
        "entries": entries,
        "buy_total": buy_total,
        "sell_total": sell_total,
        "net": sell_total - buy_total,
    }


@app.post("/ledger")
def create_ledger(data: LedgerCreate, db: sqlite3.Connection = Depends(get_db)):
    date_str = (data.date or datetime.utcnow()).isoformat()
    new_id = insert(db, "ledger", type=data.type, item=data.item, price=data.price, date=date_str)
    entry = row_dict(get_one(db, "ledger", new_id))
    return {"id": entry["id"], "type": entry["type"], "item": entry["item"], "price": entry["price"], "date": entry["date"]}


@app.delete("/ledger/{entry_id}")
def delete_ledger(entry_id: int, db: sqlite3.Connection = Depends(get_db)):
    get_or_404(db, "ledger", entry_id, "Entry not found")
    delete(db, "ledger", entry_id)
    return {"ok": True}


# ── Analysis ──────────────────────────────────────────────────

@app.get("/analysis/compatibility")
def compatibility(pc_id: Optional[int] = None, db: sqlite3.Connection = Depends(get_db)):
    return check_compatibility(parts_data_of(_owned_or_pc_parts(db, pc_id)))


@app.get("/analysis/bottleneck")
def bottleneck(pc_id: Optional[int] = None, db: sqlite3.Connection = Depends(get_db)):
    return analyze_bottleneck(parts_data_of(_owned_or_pc_parts(db, pc_id)))


@app.get("/analysis/recommend")
def recommend(purpose: str = "gaming", db: sqlite3.Connection = Depends(get_db)):
    parts = [row_dict(r) for r in db.execute("SELECT * FROM parts").fetchall()]
    parts_data = [{"category": p["category"], "brand": p["brand"], "model": p["model"], "specs": p["specs"] or {}, "owned": p["owned"]} for p in parts]
    return recommend_build(parts_data, purpose)


# ── Price ─────────────────────────────────────────────────────

PRICE_TTL = timedelta(hours=24)  # 시세는 크게 안 변하니 하루 캐시


def _cached_prices(db: sqlite3.Connection, part_id: int):
    """24시간 내 캐시가 있으면 반환, 없으면 None"""
    rows = db.execute("SELECT * FROM price_cache WHERE part_id = ?", (part_id,)).fetchall()
    if not rows:
        return None
    fetched_ats = [datetime.fromisoformat(r["fetched_at"]) for r in rows if r["fetched_at"]]
    newest = max(fetched_ats, default=None)
    if not newest or datetime.utcnow() - newest > PRICE_TTL:
        return None
    return [{"source": r["source"], "title": r["title"], "price": r["price"], "url": r["url"],
             "condition": "new" if r["source"] == "danawa" else "used"}
            for r in rows if r["source"] != "none"]  # "none" = 매물 0건 마커


def _store_prices(db: sqlite3.Connection, part_id: int, prices: list[dict]):
    db.execute("DELETE FROM price_cache WHERE part_id = ?", (part_id,))
    ts = now()
    rows = prices or [{"source": "none", "price": 0, "url": "", "title": ""}]
    db.executemany(
        "INSERT INTO price_cache (part_id, source, price, url, title, fetched_at) VALUES (?, ?, ?, ?, ?, ?)",
        [(part_id, p["source"], p["price"], p.get("url", ""), p.get("title", ""), ts) for p in rows],
    )
    db.commit()


async def get_prices_cached(db: sqlite3.Connection, part: dict, refresh: bool = False) -> tuple[list[dict], bool]:
    """(가격목록, 캐시사용여부). refresh=True면 강제 재조회"""
    if not refresh:
        cached = _cached_prices(db, part["id"])
        if cached is not None:
            return cached, True
    prices = await get_part_prices(part["brand"] or "", part["model"] or "", part["category"])
    _store_prices(db, part["id"], prices)
    return prices, False


@app.get("/prices/pc/total")
async def get_total_pc_value(pc_id: Optional[int] = None, refresh: bool = False, db: sqlite3.Connection = Depends(get_db)):
    parts = _owned_or_pc_parts(db, pc_id)

    # 부품별 시세를 병렬 조회 (캐시 히트는 즉시 반환됨)
    results = await asyncio.gather(*[get_prices_cached(db, p, refresh) for p in parts])

    parts_with_prices = [
        {
            "part": {"id": part["id"], "category": part["category"], "brand": part["brand"], "model": part["model"]},
            "prices": prices,
            "cached": cached,
        }
        for part, (prices, cached) in zip(parts, results)
    ]
    return calculate_pc_value(parts_with_prices)


@app.get("/prices/search")
async def search_deals(query: str, db: sqlite3.Connection = Depends(get_db)):
    """가성비 매물 검색 (완본체 매물도 포함, 0원 매물만 제외)"""
    from crawler import search_bunjang, search_junggo, search_danawa_direct
    import aiohttp
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
    all_results = [r for r in all_results if r.get("price", 0) > 0]
    all_results.sort(key=lambda x: (x.get("condition") != "used", x.get("price", 0)))
    return all_results


@app.get("/prices/{part_id}")
async def get_price(part_id: int, refresh: bool = False, db: sqlite3.Connection = Depends(get_db)):
    part = row_dict(get_or_404(db, "parts", part_id, "Part not found"))
    prices, cached = await get_prices_cached(db, part, refresh)
    return {"part_id": part_id, "prices": prices, "cached": cached}


# ── Parts DB Search ───────────────────────────────────────────

@app.get("/db/search")
def db_search(q: str = "", category: str = ""):
    return search_parts(q, category)


# ── Backup ────────────────────────────────────────────────────

@app.get("/backup")
def backup(db: sqlite3.Connection = Depends(get_db)):
    """전체 데이터 JSON 덤프 (프론트에서 파일로 다운로드)"""
    parts = [row_dict(r) for r in db.execute("SELECT * FROM parts").fetchall()]
    pcs = [row_dict(r) for r in db.execute("SELECT * FROM pcs").fetchall()]
    ledger = [row_dict(r) for r in db.execute("SELECT * FROM ledger").fetchall()]
    return {
        "exported_at": datetime.utcnow().isoformat(),
        "parts": [{"id": p["id"], "category": p["category"], "brand": p["brand"], "model": p["model"],
                   "specs": p["specs"], "condition": p["condition"], "owned": p["owned"],
                   "purchase_price": p["purchase_price"], "market_price": p["market_price"],
                   "pc_id": p["pc_id"], "created_at": p["created_at"]}
                  for p in parts],
        "pcs": [{"id": pc["id"], "name": pc["name"], "status": pc["status"], "whole": pc["whole"],
                 "purchase_price": pc["purchase_price"], "sold_price": pc["sold_price"],
                 "created_at": pc["created_at"], "completed_at": pc["completed_at"], "sold_at": pc["sold_at"]}
                for pc in pcs],
        "ledger": [{"id": e["id"], "type": e["type"], "item": e["item"], "price": e["price"],
                    "pc_id": e["pc_id"], "date": e["date"]}
                   for e in ledger],
    }


# ── Stats (HUD) ───────────────────────────────────────────────

@app.get("/stats")
def stats(db: sqlite3.Connection = Depends(get_db)):
    total = db.execute("SELECT COUNT(*) FROM parts").fetchone()[0]
    warehouse = db.execute("SELECT COUNT(*) FROM parts WHERE pc_id IS NULL AND owned = 1").fetchone()[0]
    wishlist = db.execute("SELECT COUNT(*) FROM parts WHERE owned = 0").fetchone()[0]
    building = db.execute("SELECT COUNT(*) FROM pcs WHERE status = 'building'").fetchone()[0]
    done = db.execute("SELECT COUNT(*) FROM pcs WHERE status = 'done'").fetchone()[0]
    sold = db.execute("SELECT COUNT(*) FROM pcs WHERE status = 'sold'").fetchone()[0]
    buy_total = db.execute("SELECT COALESCE(SUM(price), 0) FROM ledger WHERE type = 'buy'").fetchone()[0]
    sell_total = db.execute("SELECT COALESCE(SUM(price), 0) FROM ledger WHERE type = 'sell'").fetchone()[0]
    return {
        "total": total, "warehouse": warehouse, "wishlist": wishlist,
        "building": building, "done": done, "sold": sold,
        "buy_total": buy_total, "sell_total": sell_total, "net": sell_total - buy_total,
    }
