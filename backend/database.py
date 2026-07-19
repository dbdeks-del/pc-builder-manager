"""
SQLite 데이터 계층 — 표준 라이브러리 sqlite3만 사용 (SQLAlchemy 없음)
"""
import json
import os
import sqlite3
from datetime import datetime

from paths import data_dir

DB_PATH = os.path.join(data_dir(), "pc_builder.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS parts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    brand TEXT,
    model TEXT,
    specs TEXT DEFAULT '{}',
    condition TEXT DEFAULT 'used',
    owned INTEGER DEFAULT 1,
    purchase_price REAL,
    market_price REAL,
    pc_id INTEGER,
    created_at TEXT,
    updated_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_parts_category ON parts(category);
CREATE INDEX IF NOT EXISTS idx_parts_pc_id ON parts(pc_id);

CREATE TABLE IF NOT EXISTS pcs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT DEFAULT '새 PC',
    status TEXT DEFAULT 'building',
    whole INTEGER DEFAULT 0,
    purchase_price REAL,
    sold_price REAL,
    created_at TEXT,
    completed_at TEXT,
    sold_at TEXT
);

CREATE TABLE IF NOT EXISTS ledger (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    item TEXT,
    price REAL DEFAULT 0,
    pc_id INTEGER,
    date TEXT
);

CREATE TABLE IF NOT EXISTS price_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    part_id INTEGER,
    source TEXT,
    price REAL,
    url TEXT,
    title TEXT,
    fetched_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_price_cache_part_id ON price_cache(part_id);
"""


def now() -> str:
    return datetime.utcnow().isoformat()


def get_conn() -> sqlite3.Connection:
    # check_same_thread=False: FastAPI가 동기 Depends를 스레드풀에서 실행하기 때문에
    # 하나의 요청 안에서도 커넥션이 다른 스레드로 넘어갈 수 있다. 커넥션은 요청마다
    # 새로 열고 끝나면 닫으므로(get_db) 스레드 간 동시 접근은 발생하지 않아 안전하다.
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_conn()
    try:
        conn.executescript(SCHEMA)
        conn.commit()
    finally:
        conn.close()


def get_db():
    """FastAPI Depends용 제너레이터 — 요청마다 커넥션을 열고 끝나면 닫는다"""
    conn = get_conn()
    try:
        yield conn
    finally:
        conn.close()


# ── 범용 CRUD 헬퍼 (테이블/컬럼명은 항상 코드에서 오는 리터럴이라 안전) ──

def insert(conn: sqlite3.Connection, table: str, **fields) -> int:
    cols = ", ".join(fields)
    qs = ", ".join("?" for _ in fields)
    cur = conn.execute(f"INSERT INTO {table} ({cols}) VALUES ({qs})", tuple(fields.values()))
    conn.commit()
    return cur.lastrowid


def update(conn: sqlite3.Connection, table: str, row_id: int, **fields):
    if not fields:
        return
    set_clause = ", ".join(f"{k} = ?" for k in fields)
    conn.execute(f"UPDATE {table} SET {set_clause} WHERE id = ?", (*fields.values(), row_id))
    conn.commit()


def delete(conn: sqlite3.Connection, table: str, row_id: int):
    conn.execute(f"DELETE FROM {table} WHERE id = ?", (row_id,))
    conn.commit()


def get_one(conn: sqlite3.Connection, table: str, row_id: int) -> sqlite3.Row | None:
    return conn.execute(f"SELECT * FROM {table} WHERE id = ?", (row_id,)).fetchone()


def row_dict(row: sqlite3.Row | None) -> dict | None:
    """sqlite3.Row → 일반 dict. specs는 JSON 파싱, owned/whole은 bool로 변환."""
    if row is None:
        return None
    d = dict(row)
    if "specs" in d:
        d["specs"] = json.loads(d["specs"] or "{}")
    if "owned" in d:
        d["owned"] = bool(d["owned"])
    if "whole" in d:
        d["whole"] = bool(d["whole"])
    return d
