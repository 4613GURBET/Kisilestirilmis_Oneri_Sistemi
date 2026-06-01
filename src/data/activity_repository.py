"""
src/data/activity_repository.py
Sorumlu: Gurbet
"""

from sqlalchemy.orm import Session
from src.data.base_repository import BaseRepository
from src.data.models import Activity, ActivityCategory, DifficultyLevel


class ActivityRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(Activity, session)

    def get_by_category(self, category: ActivityCategory):
        return self.session.query(Activity).filter(
            Activity.category == category,
            Activity.is_active == True
        ).all()

    def get_by_difficulty(self, difficulty: DifficultyLevel):
        return self.session.query(Activity).filter(
            Activity.difficulty == difficulty,
            Activity.is_active == True
        ).all()

    def get_indoor_activities(self):
        return self.session.query(Activity).filter(
            Activity.is_indoor == True,
            Activity.is_active == True
        ).all()

    def get_by_budget(self, max_budget: float):
        return self.session.query(Activity).filter(
            Activity.min_budget <= max_budget,
            Activity.is_active == True
        ).all()