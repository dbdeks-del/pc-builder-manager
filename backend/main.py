from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import asyncio

from database import init_db, get_db
from models import Part, PCBuild, LedgerEntry, PriceCache
from compatibility import check_compatibility, analyze_bottleneck, recommend_build
from crawler import get_part_prices, calculate_pc_value
from parts_db import search_parts
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

def part_dict(p: Part) -> dict:
    perf = part_performance(p.category, p.brand or "", p.model or "", p.specs or {})
    return {
        "id": p.id, "category": p.category, "brand": p.brand, "model": p.model,
        "specs": p.specs or {}, "condition": p.condition, "owned": p.owned,
        "purchase_price": p.purchase_price, "market_price": p.market_price,
        "pc_id": p.pc_id, "rarity": perf["rarity"], "percentile": perf["percentile"],
    }


def parts_data_of(parts: list[Part]) -> list[dict]:
    return [{"category": p.category, "brand": p.brand or "", "model": p.model or "", "specs": p.specs or {}} for p in parts]


def pc_dict(pc: PCBuild, db: Session, purpose: str = "gaming") -> dict:
    parts = db.query(Part).filter(Part.pc_id == pc.id).all()
    cost = pc.purchase_price if pc.whole and pc.purchase_price else sum(p.purchase_price or 0 for p in parts)
    score = score_build(parts_data_of(parts), purpose, cost or None)
    return {
        "id": pc.id, "name": pc.name, "status": pc.status, "whole": pc.whole,
        "purchase_price": pc.purchase_price, "sold_price": pc.sold_price,
        "created_at": pc.created_at, "completed_at": pc.completed_at, "sold_at": pc.sold_at,
        "parts": [part_dict(p) for p in parts],
        "cost": cost,
        "score": score,
    }


# ── Parts CRUD ────────────────────────────────────────────────

@app.get("/parts")
def list_parts(owned: Optional[bool] = None, in_warehouse: Optional[bool] = None, db: Session = Depends(get_db)):
    q = db.query(Part)
    if owned is not None:
        q = q.filter(Part.owned == owned)
    if in_warehouse:
        q = q.filter(Part.pc_id.is_(None))
    return [part_dict(p) for p in q.order_by(Part.id.desc()).all()]


@app.post("/parts")
def create_part(data: PartCreate, db: Session = Depends(get_db)):
    part = Part(**data.model_dump())
    db.add(part)
    db.commit()
    db.refresh(part)
    return part_dict(part)


@app.put("/parts/{part_id}")
def update_part(part_id: int, data: PartUpdate, db: Session = Depends(get_db)):
    part = db.query(Part).filter(Part.id == part_id).first()
    if not part:
        raise HTTPException(404, "Part not found")
    for k, v in data.model_dump(exclude_none=True).items():
        setattr(part, k, v)
    db.commit()
    db.refresh(part)
    return part_dict(part)


@app.delete("/parts/{part_id}")
def delete_part(part_id: int, db: Session = Depends(get_db)):
    part = db.query(Part).filter(Part.id == part_id).first()
    if not part:
        raise HTTPException(404, "Part not found")
    db.delete(part)
    db.commit()
    return {"ok": True}


@app.post("/parts/{part_id}/sell")
def sell_part(part_id: int, data: SellRequest, db: Session = Depends(get_db)):
    """부품 개별 판매: 장부에 기록하고 인벤토리에서 제거"""
    part = db.query(Part).filter(Part.id == part_id).first()
    if not part:
        raise HTTPException(404, "Part not found")
    if part.pc_id is not None:
        raise HTTPException(400, "PC에 장착된 부품입니다. 먼저 탈착하세요.")
    name = f"{part.brand or ''} {part.model or ''}".strip()
    margin = data.price - (part.purchase_price or 0)
    db.add(LedgerEntry(type="sell", item=f"[부품판매] {name}", price=data.price))
    db.delete(part)
    db.commit()
    return {"ok": True, "margin": margin}


# ── PC 조립 (조립실) ──────────────────────────────────────────

@app.get("/pcs")
def list_pcs(status: Optional[str] = None, purpose: str = "gaming", db: Session = Depends(get_db)):
    q = db.query(PCBuild)
    if status:
        q = q.filter(PCBuild.status == status)
    return [pc_dict(pc, db, purpose) for pc in q.order_by(PCBuild.id.desc()).all()]


@app.post("/pcs")
def create_pc(data: PCCreate, db: Session = Depends(get_db)):
    pc = PCBuild(name=data.name)
    db.add(pc)
    db.commit()
    db.refresh(pc)
    return pc_dict(pc, db)


@app.get("/pcs/{pc_id}")
def get_pc(pc_id: int, purpose: str = "gaming", db: Session = Depends(get_db)):
    pc = db.query(PCBuild).filter(PCBuild.id == pc_id).first()
    if not pc:
        raise HTTPException(404, "PC not found")
    return pc_dict(pc, db, purpose)


@app.put("/pcs/{pc_id}")
def update_pc(pc_id: int, data: PCUpdate, db: Session = Depends(get_db)):
    pc = db.query(PCBuild).filter(PCBuild.id == pc_id).first()
    if not pc:
        raise HTTPException(404, "PC not found")
    for k, v in data.model_dump(exclude_none=True).items():
        setattr(pc, k, v)
    db.commit()
    return pc_dict(pc, db)


@app.post("/pcs/{pc_id}/parts/{part_id}")
def attach_part(pc_id: int, part_id: int, db: Session = Depends(get_db)):
    pc = db.query(PCBuild).filter(PCBuild.id == pc_id).first()
    part = db.query(Part).filter(Part.id == part_id).first()
    if not pc or not part:
        raise HTTPException(404, "PC or Part not found")
    if part.pc_id is not None and part.pc_id != pc_id:
        raise HTTPException(400, "이미 다른 PC에 장착된 부품입니다.")
    part.pc_id = pc_id
    db.commit()
    return pc_dict(pc, db)


@app.delete("/pcs/{pc_id}/parts/{part_id}")
def detach_part(pc_id: int, part_id: int, db: Session = Depends(get_db)):
    part = db.query(Part).filter(Part.id == part_id, Part.pc_id == pc_id).first()
    if not part:
        raise HTTPException(404, "Part not found on this PC")
    part.pc_id = None
    db.commit()
    pc = db.query(PCBuild).filter(PCBuild.id == pc_id).first()
    return pc_dict(pc, db)


@app.post("/pcs/{pc_id}/complete")
def complete_pc(pc_id: int, db: Session = Depends(get_db)):
    pc = db.query(PCBuild).filter(PCBuild.id == pc_id).first()
    if not pc:
        raise HTTPException(404, "PC not found")
    pc.status = "done"
    pc.completed_at = datetime.utcnow()
    db.commit()
    return pc_dict(pc, db)


@app.post("/pcs/{pc_id}/reopen")
def reopen_pc(pc_id: int, db: Session = Depends(get_db)):
    pc = db.query(PCBuild).filter(PCBuild.id == pc_id).first()
    if not pc:
        raise HTTPException(404, "PC not found")
    pc.status = "building"
    pc.completed_at = None
    db.commit()
    return pc_dict(pc, db)


@app.post("/pcs/{pc_id}/sell")
def sell_pc(pc_id: int, data: SellRequest, db: Session = Depends(get_db)):
    pc = db.query(PCBuild).filter(PCBuild.id == pc_id).first()
    if not pc:
        raise HTTPException(404, "PC not found")
    pc.status = "sold"
    pc.sold_price = data.price
    pc.sold_at = datetime.utcnow()
    db.add(LedgerEntry(type="sell", item=pc.name, price=data.price, pc_id=pc.id))
    db.commit()
    return pc_dict(pc, db)


@app.post("/pcs/{pc_id}/dismantle")
def dismantle_pc(pc_id: int, db: Session = Depends(get_db)):
    """해체: 부품은 창고로 복귀, PC 카드는 삭제 (장부 기록은 유지)"""
    pc = db.query(PCBuild).filter(PCBuild.id == pc_id).first()
    if not pc:
        raise HTTPException(404, "PC not found")
    for part in db.query(Part).filter(Part.pc_id == pc_id).all():
        part.pc_id = None
    db.delete(pc)
    db.commit()
    return {"ok": True}


@app.delete("/pcs/{pc_id}")
def delete_pc(pc_id: int, db: Session = Depends(get_db)):
    """삭제: 부품까지 함께 삭제"""
    pc = db.query(PCBuild).filter(PCBuild.id == pc_id).first()
    if not pc:
        raise HTTPException(404, "PC not found")
    db.query(Part).filter(Part.pc_id == pc_id).delete()
    db.delete(pc)
    db.commit()
    return {"ok": True}


@app.post("/pcs/whole")
def whole_intake(data: WholeIntake, db: Session = Depends(get_db)):
    """본체 통째 매입: 완성 PC + 부품들 + 구매 장부를 한 번에 생성"""
    pc = PCBuild(name=data.name, status="done", whole=True,
                 purchase_price=data.purchase_price, completed_at=datetime.utcnow())
    db.add(pc)
    db.flush()
    for wp in data.parts:
        db.add(Part(category=wp.category, brand=wp.brand, model=wp.model,
                    specs=wp.specs, pc_id=pc.id))
    db.add(LedgerEntry(type="buy", item=f"[통매입] {data.name}", price=data.purchase_price, pc_id=pc.id))
    db.commit()
    return pc_dict(pc, db)


# ── 종합점수 (검사실) ─────────────────────────────────────────

@app.get("/pcs/{pc_id}/score")
def pc_score(pc_id: int, purpose: str = "gaming", db: Session = Depends(get_db)):
    pc = db.query(PCBuild).filter(PCBuild.id == pc_id).first()
    if not pc:
        raise HTTPException(404, "PC not found")
    parts = db.query(Part).filter(Part.pc_id == pc_id).all()
    cost = pc.purchase_price if pc.whole and pc.purchase_price else sum(p.purchase_price or 0 for p in parts)
    return score_build(parts_data_of(parts), purpose, cost or None)


# ── 장부 ──────────────────────────────────────────────────────

@app.get("/ledger")
def list_ledger(db: Session = Depends(get_db)):
    entries = db.query(LedgerEntry).order_by(LedgerEntry.date.desc(), LedgerEntry.id.desc()).all()
    buy_total = sum(e.price or 0 for e in entries if e.type == "buy")
    sell_total = sum(e.price or 0 for e in entries if e.type == "sell")
    return {
        "entries": [{"id": e.id, "type": e.type, "item": e.item, "price": e.price,
                     "pc_id": e.pc_id, "date": e.date} for e in entries],
        "buy_total": buy_total,
        "sell_total": sell_total,
        "net": sell_total - buy_total,
    }


@app.post("/ledger")
def create_ledger(data: LedgerCreate, db: Session = Depends(get_db)):
    entry = LedgerEntry(type=data.type, item=data.item, price=data.price,
                        date=data.date or datetime.utcnow())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return {"id": entry.id, "type": entry.type, "item": entry.item, "price": entry.price, "date": entry.date}


@app.delete("/ledger/{entry_id}")
def delete_ledger(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(LedgerEntry).filter(LedgerEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(404, "Entry not found")
    db.delete(entry)
    db.commit()
    return {"ok": True}


# ── Analysis ──────────────────────────────────────────────────

@app.get("/analysis/compatibility")
def compatibility(pc_id: Optional[int] = None, db: Session = Depends(get_db)):
    q = db.query(Part).filter(Part.owned == True)
    if pc_id is not None:
        q = db.query(Part).filter(Part.pc_id == pc_id)
    return check_compatibility(parts_data_of(q.all()))


@app.get("/analysis/bottleneck")
def bottleneck(pc_id: Optional[int] = None, db: Session = Depends(get_db)):
    q = db.query(Part).filter(Part.owned == True)
    if pc_id is not None:
        q = db.query(Part).filter(Part.pc_id == pc_id)
    return analyze_bottleneck(parts_data_of(q.all()))


@app.get("/analysis/recommend")
def recommend(purpose: str = "gaming", db: Session = Depends(get_db)):
    parts = db.query(Part).all()
    parts_data = [{"category": p.category, "brand": p.brand, "model": p.model, "specs": p.specs or {}, "owned": p.owned} for p in parts]
    return recommend_build(parts_data, purpose)


# ── Price ─────────────────────────────────────────────────────

PRICE_TTL = timedelta(hours=24)  # 시세는 크게 안 변하니 하루 캐시


def _cached_prices(db: Session, part_id: int):
    """24시간 내 캐시가 있으면 반환, 없으면 None"""
    rows = db.query(PriceCache).filter(PriceCache.part_id == part_id).all()
    if not rows:
        return None
    newest = max((r.fetched_at for r in rows if r.fetched_at), default=None)
    if not newest or datetime.utcnow() - newest > PRICE_TTL:
        return None
    return [{"source": r.source, "title": r.title, "price": r.price, "url": r.url,
             "condition": "new" if r.source == "danawa" else "used"}
            for r in rows if r.source != "none"]  # "none" = 매물 0건 마커


def _store_prices(db: Session, part_id: int, prices: list[dict]):
    db.query(PriceCache).filter(PriceCache.part_id == part_id).delete()
    for p in prices:
        db.add(PriceCache(part_id=part_id, source=p["source"], price=p["price"],
                          url=p.get("url", ""), title=p.get("title", "")))
    if not prices:  # 매물 0건도 캐시해서 매번 재크롤링하지 않게
        db.add(PriceCache(part_id=part_id, source="none", price=0, url="", title=""))
    db.commit()


async def get_prices_cached(db: Session, part: Part, refresh: bool = False) -> tuple[list[dict], bool]:
    """(가격목록, 캐시사용여부). refresh=True면 강제 재조회"""
    if not refresh:
        cached = _cached_prices(db, part.id)
        if cached is not None:
            return cached, True
    prices = await get_part_prices(part.brand or "", part.model or "", part.category)
    _store_prices(db, part.id, prices)
    return prices, False


@app.get("/prices/pc/total")
async def get_total_pc_value(pc_id: Optional[int] = None, refresh: bool = False, db: Session = Depends(get_db)):
    q = db.query(Part).filter(Part.owned == True)
    if pc_id is not None:
        q = db.query(Part).filter(Part.pc_id == pc_id)
    parts = q.all()

    # 부품별 시세를 병렬 조회 (캐시 히트는 즉시 반환됨)
    results = await asyncio.gather(*[get_prices_cached(db, p, refresh) for p in parts])

    parts_with_prices = [
        {
            "part": {"id": part.id, "category": part.category, "brand": part.brand, "model": part.model},
            "prices": prices,
            "cached": cached,
        }
        for part, (prices, cached) in zip(parts, results)
    ]
    return calculate_pc_value(parts_with_prices)


@app.get("/prices/search")
async def search_deals(query: str, db: Session = Depends(get_db)):
    """가성비 매물 검색 (완본체 매물도 포함, 0원 매물만 제외)"""
    from crawler import search_bunjang, search_junggo, search_danawa_direct
    tasks = [
        search_danawa_direct(query),
        search_bunjang(query),
        search_junggo(query),
    ]
    results_list = await asyncio.gather(*tasks, return_exceptions=True)
    all_results = []
    for r in results_list:
        if isinstance(r, list):
            all_results.extend(r)
    all_results = [r for r in all_results if r.get("price", 0) > 0]
    all_results.sort(key=lambda x: (x.get("condition") != "used", x.get("price", 0)))
    return all_results


@app.get("/prices/{part_id}")
async def get_price(part_id: int, refresh: bool = False, db: Session = Depends(get_db)):
    part = db.query(Part).filter(Part.id == part_id).first()
    if not part:
        raise HTTPException(404, "Part not found")
    prices, cached = await get_prices_cached(db, part, refresh)
    return {"part_id": part_id, "prices": prices, "cached": cached}


# ── Parts DB Search ───────────────────────────────────────────

@app.get("/db/search")
def db_search(q: str = "", category: str = ""):
    return search_parts(q, category)


# ── Backup ────────────────────────────────────────────────────

@app.get("/backup")
def backup(db: Session = Depends(get_db)):
    """전체 데이터 JSON 덤프 (프론트에서 파일로 다운로드)"""
    parts = db.query(Part).all()
    pcs = db.query(PCBuild).all()
    ledger = db.query(LedgerEntry).all()
    return {
        "exported_at": datetime.utcnow().isoformat(),
        "parts": [{"id": p.id, "category": p.category, "brand": p.brand, "model": p.model,
                   "specs": p.specs, "condition": p.condition, "owned": p.owned,
                   "purchase_price": p.purchase_price, "market_price": p.market_price,
                   "pc_id": p.pc_id, "created_at": p.created_at.isoformat() if p.created_at else None}
                  for p in parts],
        "pcs": [{"id": pc.id, "name": pc.name, "status": pc.status, "whole": pc.whole,
                 "purchase_price": pc.purchase_price, "sold_price": pc.sold_price,
                 "created_at": pc.created_at.isoformat() if pc.created_at else None,
                 "completed_at": pc.completed_at.isoformat() if pc.completed_at else None,
                 "sold_at": pc.sold_at.isoformat() if pc.sold_at else None}
                for pc in pcs],
        "ledger": [{"id": e.id, "type": e.type, "item": e.item, "price": e.price,
                    "pc_id": e.pc_id, "date": e.date.isoformat() if e.date else None}
                   for e in ledger],
    }


# ── Stats (HUD) ───────────────────────────────────────────────

@app.get("/stats")
def stats(db: Session = Depends(get_db)):
    total = db.query(Part).count()
    warehouse = db.query(Part).filter(Part.pc_id.is_(None), Part.owned == True).count()
    wishlist = db.query(Part).filter(Part.owned == False).count()
    building = db.query(PCBuild).filter(PCBuild.status == "building").count()
    done = db.query(PCBuild).filter(PCBuild.status == "done").count()
    sold = db.query(PCBuild).filter(PCBuild.status == "sold").count()
    entries = db.query(LedgerEntry).all()
    buy_total = sum(e.price or 0 for e in entries if e.type == "buy")
    sell_total = sum(e.price or 0 for e in entries if e.type == "sell")
    return {
        "total": total, "warehouse": warehouse, "wishlist": wishlist,
        "building": building, "done": done, "sold": sold,
        "buy_total": buy_total, "sell_total": sell_total, "net": sell_total - buy_total,
    }
