"""
tests/test_activity_service.py
Sorumlu: Efe
Mock ile business katmanı testleri
"""

import pytest
from unittest.mock import MagicMock, patch
from src.business.activity_service import ActivityService
from src.data.models import Activity, ActivityCategory, DifficultyLevel


@pytest.fixture
def mock_repos():
    activity_repo = MagicMock()
    user_repo     = MagicMock()
    return activity_repo, user_repo


@pytest.fixture
def mock_engine():
    engine = MagicMock()
    engine.predict.return_value = [{"activity_id": 1, "confidence": 0.92}]
    return engine


@pytest.fixture
def mock_ai():
    ai = MagicMock()
    ai.generate_note.return_value = "Bugün harika bir aktivite seni bekliyor!"
    return ai


def test_get_recommendations_returns_list(mock_repos, mock_engine, mock_ai):
    activity_repo, user_repo = mock_repos

    # Kullanıcı mock'u
    user = MagicMock()
    user.preferences.age = 25
    user.preferences.preferred_category.value = "sports"
    user.preferences.max_duration_minutes = 60
    user.preferences.preferred_difficulty.value = "medium"
    user.preferences.indoor_preference = True
    user.preferences.budget_range = 100.0
    user_repo.get_by_id.return_value = user

    # Aktivite mock'u
    activity = Activity(
        id=1, name="Yüzme",
        category=ActivityCategory.SPORTS,
        difficulty=DifficultyLevel.MEDIUM
    )
    activity_repo.get_by_id.return_value = activity

    service = ActivityService(activity_repo, user_repo, mock_engine, mock_ai)
    results = service.get_recommendations(1)

    assert len(results) == 1
    assert results[0]["activity"].name == "Yüzme"
    assert results[0]["ai_note"] == "Bugün harika bir aktivite seni bekliyor!"


def test_get_recommendations_no_user(mock_repos, mock_engine, mock_ai):
    activity_repo, user_repo = mock_repos
    user_repo.get_by_id.return_value = None

    service = ActivityService(activity_repo, user_repo, mock_engine, mock_ai)
    results = service.get_recommendations(999)

    assert results == []