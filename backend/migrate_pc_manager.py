"""
PC-Manager(data.json) → PC Builder Manager(SQLite) 데이터 마이그레이션

사용법:
    python migrate_pc_manager.py <data.json 경로>

- 창고 부품 / 조립중·완성 PC(장착 부품 포함) / 장부 기록을 모두 이전
- 원본 data.json은 수정하지 않음
- 여러 번 실행하면 중복 저장되므로 1회만 실행 권장
"""
import json
import sys
from datetime import datetime

from database import init_db, SessionLocal
from models import Part, PCBuild, LedgerEntry
from parts_db import KO2EN


def parse_date(s: str | None) -> datetime:
    if not s:
        return datetime.utcnow()
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    return datetime.utcnow()


def map_category(ko_cat: str, name: str, spec: str) -> str:
    cat = KO2EN.get(ko_cat, "etc")
    if ko_cat == "저장장치":
        text = f"{name} {spec}".upper()
        if "HDD" in text or "하드" in text:
            return "hdd"
        return "ssd"
    return cat


def to_part(old: dict, pc_id: int | None = None) -> Part:
    name = (old.get("name") or "").strip()
    tokens = name.split(None, 1)
    brand, model = (tokens[0], tokens[1]) if len(tokens) == 2 else ("", name)
    spec = old.get("spec") or ""
    return Part(
        category=map_category(old.get("cat", "기타"), name, spec),
        brand=brand,
        model=model,
        specs={"summary": spec} if spec else {},
        condition="used",
        owned=True,
        purchase_price=old.get("price") or None,
        market_price=old.get("marketPrice") or None,
        pc_id=pc_id,
        created_at=parse_date(old.get("added")),
    )


def migrate(path: str):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    init_db()
    db = SessionLocal()
    try:
        n_parts = n_pcs = n_ledger = 0

        # 창고 부품
        for old in data.get("parts", []):
            db.add(to_part(old))
            n_parts += 1

        # PC (장착 부품 포함)
        for old_pc in data.get("pcs", []):
            status = old_pc.get("status", "building")
            if status not in ("building", "done", "sold"):
                status = "building"
            pc = PCBuild(
                name=old_pc.get("name", "이름 없음"),
                status="sold" if old_pc.get("soldPrice") else status,
                whole=bool(old_pc.get("whole")),
                purchase_price=old_pc.get("purchasePrice") or None,
                sold_price=old_pc.get("soldPrice") or None,
                created_at=parse_date(old_pc.get("created") or old_pc.get("purchaseDate")),
                completed_at=parse_date(old_pc.get("completed")) if old_pc.get("completed") else None,
            )
            db.add(pc)
            db.flush()
            for old_part in old_pc.get("parts", []):
                db.add(to_part(old_part, pc_id=pc.id))
                n_parts += 1
            n_pcs += 1

        # 장부
        for old in data.get("ledger", []):
            db.add(LedgerEntry(
                type=old.get("type", "buy"),
                item=old.get("item", ""),
                price=old.get("price") or 0,
                date=parse_date(old.get("date")),
            ))
            n_ledger += 1

        db.commit()
        print(f"마이그레이션 완료: 부품 {n_parts}개, PC {n_pcs}대, 장부 {n_ledger}건")
    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python migrate_pc_manager.py <data.json 경로>")
        sys.exit(1)
    migrate(sys.argv[1])
