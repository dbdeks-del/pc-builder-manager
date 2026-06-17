from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import asyncio

from database import init_db, get_db
from models import Part, PriceCache
from compatibility import check_compatibility, analyze_bottleneck, recommend_build
from crawler import get_part_prices, calculate_pc_value
from parts_db import search_parts

app = FastAPI(title="PC Builder Manager", version="1.0.0")

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
    brand: str
    model: str
    specs: dict = {}
    condition: str = "used"
    owned: bool = True
    purchase_price: Optional[float] = None


class PartUpdate(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    specs: Optional[dict] = None
    condition: Optional[str] = None
    owned: Optional[bool] = None
    purchase_price: Optional[float] = None


# ── Parts CRUD ────────────────────────────────────────────────

@app.get("/parts")
def list_parts(owned: Optional[bool] = None, db: Session = Depends(get_db)):
    q = db.query(Part)
    if owned is not None:
        q = q.filter(Part.owned == owned)
    return q.all()


@app.post("/parts")
def create_part(data: PartCreate, db: Session = Depends(get_db)):
    part = Part(**data.model_dump())
    db.add(part)
    db.commit()
    db.refresh(part)
    return part


@app.put("/parts/{part_id}")
def update_part(part_id: int, data: PartUpdate, db: Session = Depends(get_db)):
    part = db.query(Part).filter(Part.id == part_id).first()
    if not part:
        raise HTTPException(404, "Part not found")
    for k, v in data.model_dump(exclude_none=True).items():
        setattr(part, k, v)
    db.commit()
    db.refresh(part)
    return part


@app.delete("/parts/{part_id}")
def delete_part(part_id: int, db: Session = Depends(get_db)):
    part = db.query(Part).filter(Part.id == part_id).first()
    if not part:
        raise HTTPException(404, "Part not found")
    db.delete(part)
    db.commit()
    return {"ok": True}


# ── Analysis ──────────────────────────────────────────────────

@app.get("/analysis/compatibility")
def compatibility(db: Session = Depends(get_db)):
    parts = db.query(Part).filter(Part.owned == True).all()
    parts_data = [{"category": p.category, "brand": p.brand, "model": p.model, "specs": p.specs or {}} for p in parts]
    return check_compatibility(parts_data)


@app.get("/analysis/bottleneck")
def bottleneck(db: Session = Depends(get_db)):
    parts = db.query(Part).filter(Part.owned == True).all()
    parts_data = [{"category": p.category, "brand": p.brand, "model": p.model, "specs": p.specs or {}} for p in parts]
    return analyze_bottleneck(parts_data)


@app.get("/analysis/recommend")
def recommend(purpose: str = "gaming", db: Session = Depends(get_db)):
    parts = db.query(Part).all()
    parts_data = [{"category": p.category, "brand": p.brand, "model": p.model, "specs": p.specs or {}, "owned": p.owned} for p in parts]
    return recommend_build(parts_data, purpose)


# ── Price ─────────────────────────────────────────────────────

@app.get("/prices/{part_id}")
async def get_price(part_id: int, db: Session = Depends(get_db)):
    part = db.query(Part).filter(Part.id == part_id).first()
    if not part:
        raise HTTPException(404, "Part not found")

    prices = await get_part_prices(part.brand, part.model, part.category)

    # 캐시 저장
    db.query(PriceCache).filter(PriceCache.part_id == part_id).delete()
    for p in prices:
        cache = PriceCache(
            part_id=part_id,
            source=p["source"],
            price=p["price"],
            url=p.get("url", ""),
            title=p.get("title", ""),
        )
        db.add(cache)
    db.commit()

    return {"part_id": part_id, "prices": prices}


@app.get("/prices/pc/total")
async def get_total_pc_value(db: Session = Depends(get_db)):
    parts = db.query(Part).filter(Part.owned == True).all()

    parts_with_prices = []
    for part in parts:
        prices = await get_part_prices(part.brand, part.model, part.category)
        parts_with_prices.append({
            "part": {"id": part.id, "category": part.category, "brand": part.brand, "model": part.model},
            "prices": prices,
        })

    return calculate_pc_value(parts_with_prices)


@app.get("/prices/search")
async def search_deals(query: str, db: Session = Depends(get_db)):
    """가성비 매물 검색"""
    from crawler import search_bunjang, search_junggo, search_danawa_direct
    tasks = [
        search_danawa_direct(query),
        search_bunjang(query + " 중고"),
        search_junggo(query + " 중고"),
    ]
    results_list = await asyncio.gather(*tasks, return_exceptions=True)
    all_results = []
    for r in results_list:
        if isinstance(r, list):
            all_results.extend(r)
    all_results.sort(key=lambda x: x.get("price", 0))
    return all_results


# ── Parts DB Search ───────────────────────────────────────────

@app.get("/db/search")
def db_search(q: str = "", category: str = ""):
    return search_parts(q, category)


# ── Stats ─────────────────────────────────────────────────────

@app.get("/stats")
def stats(db: Session = Depends(get_db)):
    total = db.query(Part).count()
    owned = db.query(Part).filter(Part.owned == True).count()
    wishlist = db.query(Part).filter(Part.owned == False).count()
    return {"total": total, "owned": owned, "wishlist": wishlist}
