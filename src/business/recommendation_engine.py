"""
src/business/recommendation_engine.py
Eğitilmiş modeli yükleyip öneri üreten sınıf
Katman: Business
Sorumlu: Efe
"""

import pickle
import numpy as np
from src.data.models import ActivityCategory, DifficultyLevel


class RecommendationEngine:
    def __init__(self, model_path: str = "src/business/model.pkl"):
        self.model = self._load_model(model_path)

    def _load_model(self, path: str):
        try:
            with open(path, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Model dosyası bulunamadı: {path}")

    def predict(self, user_features: dict) -> list:
        """
        Kullanıcı tercihlerine göre aktivite önerileri döndürür.
        user_features: UserPreference tablosundaki alanlarla örtüşmeli
        """
        features = self._prepare_features(user_features)
        predictions = self.model.predict(features)
        probabilities = self._get_probabilities(features)
        return self._format_results(predictions, probabilities)

    def _prepare_features(self, user_features: dict) -> np.ndarray:
        """
        Dict'i modelin beklediği numpy array'e çevirir.
        Veri temizlemede kullanılan encode sırasıyla aynı olmalı!
        """
        category_map   = {c.value: i for i, c in enumerate(ActivityCategory)}
        difficulty_map = {d.value: i for i, d in enumerate(DifficultyLevel)}

        return np.array([[
            user_features.get("age", 25),
            category_map.get(user_features.get("preferred_category", "sports"), 0),
            user_features.get("max_duration_minutes", 60),
            difficulty_map.get(user_features.get("preferred_difficulty", "medium"), 1),
            int(user_features.get("indoor_preference", True)),
            user_features.get("budget_range", 100.0),
        ]])

    def _get_probabilities(self, features: np.ndarray) -> np.ndarray:
        if hasattr(self.model, "predict_proba"):
            return self.model.predict_proba(features)[0]
        return np.array([])

    def _format_results(self, predictions, probabilities) -> list:
        results = []
        for i, pred in enumerate(predictions):
            result = {"activity_id": int(pred)}
            if len(probabilities) > i:
                result["confidence"] = round(float(probabilities[i]), 3)
            results.append(result)
        return results