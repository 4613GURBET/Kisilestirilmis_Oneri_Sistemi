"""
src/business/activity_service.py
İş mantığı katmanı — Presentation buraya çağrı yapar
Katman: Business
Sorumlu: Efe
KURAL: Bu katman DB'ye direkt dokunmaz, repository'den geçer!
"""

from src.business.recommendation_engine import RecommendationEngine
from src.business.ai_client import AIClient
from src.data.activity_repository import ActivityRepository
from src.data.user_repository import UserRepository


class ActivityService:
    def __init__(self, activity_repo: ActivityRepository,
                 user_repo: UserRepository,
                 engine: RecommendationEngine = None,
                 ai_client: AIClient = None):
        self.activity_repo = activity_repo
        self.user_repo     = user_repo
        self.engine        = engine or RecommendationEngine()
        self.ai_client     = ai_client or AIClient()

    def get_recommendations(self, user_id: int) -> list:
        """
        Kullanıcı ID'sine göre öneri listesi döndürür.
        1. Kullanıcı tercihlerini DB'den çek
        2. Modele ver, aktivite ID'leri al
        3. Her aktivite için AI notu üret
        4. Sonuçları döndür
        """
        user = self.user_repo.get_by_id(user_id)
        if not user or not user.preferences:
            return []

        prefs = user.preferences
        user_features = {
            "age":                  prefs.age,
            "preferred_category":   prefs.preferred_category.value if prefs.preferred_category else None,
            "max_duration_minutes": prefs.max_duration_minutes,
            "preferred_difficulty": prefs.preferred_difficulty.value if prefs.preferred_difficulty else None,
            "indoor_preference":    prefs.indoor_preference,
            "budget_range":         prefs.budget_range,
        }

        predictions = self.engine.predict(user_features)

        results = []
        for pred in predictions:
            activity = self.activity_repo.get_by_id(pred["activity_id"])
            if not activity:
                continue
            try:
                note = self.ai_client.generate_note(activity.name, user_features)
            except Exception:
                note = f"{activity.name} aktivitesini bugün deneyin!"

            results.append({
                "activity":   activity,
                "confidence": pred.get("confidence"),
                "ai_note":    note,
            })

        return results

    def get_all_activities(self):
        return self.activity_repo.get_all()

    def get_activities_by_category(self, category):
        return self.activity_repo.get_by_category(category)