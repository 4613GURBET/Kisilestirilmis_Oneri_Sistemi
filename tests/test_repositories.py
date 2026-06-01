"""
tests/test_repositories.py
Sorumlu: Gurbet
Mock DB ile repository testleri — gerçek DB bağlantısı gerekmez
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.data.models import Base, User, Activity, ActivityCategory, DifficultyLevel
from src.data.user_repository import UserRepository
from src.data.activity_repository import ActivityRepository


@pytest.fixture
def session():
    """Her test için temiz, in-memory SQLite DB."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    s = Session()
    yield s
    s.close()
    Base.metadata.drop_all(engine)


# ── User testleri ──────────────────────────────
def test_add_and_get_user(session):
    repo = UserRepository(session)
    user = User(username="gurbet", email="gurbet@test.com", password="hash123")
    repo.add(user)
    result = repo.get_by_email("gurbet@test.com")
    assert result is not None
    assert result.username == "gurbet"


def test_get_by_username(session):
    repo = UserRepository(session)
    user = User(username="efe", email="efe@test.com", password="hash123")
    repo.add(user)
    result = repo.get_by_username("efe")
    assert result.email == "efe@test.com"


def test_delete_user(session):
    repo = UserRepository(session)
    user = User(username="lizge", email="lizge@test.com", password="hash123")
    repo.add(user)
    repo.delete(user.id)
    assert repo.get_by_id(user.id) is None


# ── Activity testleri ──────────────────────────
def test_get_by_category(session):
    repo = ActivityRepository(session)
    activity = Activity(
        name="Yüzme",
        category=ActivityCategory.SPORTS,
        difficulty=DifficultyLevel.MEDIUM,
        is_indoor=False
    )
    repo.add(activity)
    results = repo.get_by_category(ActivityCategory.SPORTS)
    assert len(results) == 1
    assert results[0].name == "Yüzme"


def test_get_by_budget(session):
    repo = ActivityRepository(session)
    repo.add(Activity(
        name="Kitap okuma",
        category=ActivityCategory.EDUCATIONAL,
        difficulty=DifficultyLevel.EASY,
        min_budget=0.0,
        max_budget=50.0
    ))
    results = repo.get_by_budget(100.0)
    assert len(results) == 1