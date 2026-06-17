from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Part(Base):
    __tablename__ = "parts"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True)  # cpu, gpu, ram, ssd, hdd, motherboard, psu, case, cooler
    brand = Column(String)
    model = Column(String)
    specs = Column(JSON, default={})  # category-specific specs
    condition = Column(String, default="used")  # new, used, broken
    owned = Column(Boolean, default=True)  # True=보유중, False=위시리스트
    purchase_price = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PriceCache(Base):
    __tablename__ = "price_cache"

    id = Column(Integer, primary_key=True, index=True)
    part_id = Column(Integer, index=True)
    source = Column(String)  # danawa, daangn, junggo
    price = Column(Float)
    url = Column(String, nullable=True)
    title = Column(String, nullable=True)
    fetched_at = Column(DateTime, default=datetime.utcnow)
