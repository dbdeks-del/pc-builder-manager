from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Part(Base):
    __tablename__ = "parts"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True)  # cpu, gpu, ram, ssd, hdd, motherboard, psu, case, cooler, etc
    brand = Column(String)
    model = Column(String)
    specs = Column(JSON, default={})  # category-specific specs
    condition = Column(String, default="used")  # new, used, broken
    owned = Column(Boolean, default=True)  # True=보유중, False=위시리스트
    purchase_price = Column(Float, nullable=True)
    market_price = Column(Float, nullable=True)  # 수동 입력 중고 시세
    pc_id = Column(Integer, nullable=True, index=True)  # 장착된 PC (None=창고)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PCBuild(Base):
    __tablename__ = "pcs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="새 PC")
    status = Column(String, default="building")  # building, done, sold
    whole = Column(Boolean, default=False)  # 본체 통째 매입 여부
    purchase_price = Column(Float, nullable=True)  # 통매입 가격
    sold_price = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    sold_at = Column(DateTime, nullable=True)


class LedgerEntry(Base):
    __tablename__ = "ledger"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)  # buy, sell
    item = Column(String)
    price = Column(Float, default=0)
    pc_id = Column(Integer, nullable=True)
    date = Column(DateTime, default=datetime.utcnow)


class PriceCache(Base):
    __tablename__ = "price_cache"

    id = Column(Integer, primary_key=True, index=True)
    part_id = Column(Integer, index=True)
    source = Column(String)  # danawa, bunjang, junggo
    price = Column(Float)
    url = Column(String, nullable=True)
    title = Column(String, nullable=True)
    fetched_at = Column(DateTime, default=datetime.utcnow)
