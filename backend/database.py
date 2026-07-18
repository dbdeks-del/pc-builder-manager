from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "sqlite:///./pc_builder.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)
    _migrate_columns()


def _migrate_columns():
    """구버전 DB 파일에 새 컬럼 추가 (SQLite는 create_all이 기존 테이블을 안 바꿈)"""
    from sqlalchemy import text
    new_columns = {
        "parts": [
            ("market_price", "FLOAT"),
            ("pc_id", "INTEGER"),
        ],
    }
    with engine.connect() as conn:
        for table, cols in new_columns.items():
            existing = {row[1] for row in conn.execute(text(f"PRAGMA table_info({table})"))}
            for name, sqltype in cols:
                if name not in existing:
                    conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {name} {sqltype}"))
        conn.commit()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
