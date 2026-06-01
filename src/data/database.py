"""
src/data/database.py
Veritabanı bağlantısı ve session yönetimi
Sorumlu: Gurbet
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.data.models import Base
from config import Config


engine = create_engine(Config.DATABASE_URL, echo=Config.DEBUG)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_session() -> Session:
    """Flask route'larında kullanılacak session factory."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def create_tables():
    """Geliştirme ortamında tabloları oluşturur. Migration varsa kullanma."""
    Base.metadata.create_all(bind=engine)