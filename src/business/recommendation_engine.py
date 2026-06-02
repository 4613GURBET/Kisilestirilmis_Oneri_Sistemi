"""
src/business/recommendation_engine.py
Eğitilmiş modeli yükleyip öneri üreten sınıf
Katman: Business
Sorumlu: Efe
"""
import pandas as pd
import joblib
import pickle
import numpy as np
from src.data.models import ActivityCategory, DifficultyLevel


class RecommendationEngine:
    def __init__(self, model_path: str = "src/business/model.joblib"):
        self.model = self._load_model(model_path)

    def _load_model(self, path: str):
        try:
            with open(path, "rb") as f:
                return joblib.load(path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Model dosyası bulunamadı: {path}")

    def predict(self, user_features: dict) -> list:
        if self.model is None:
            return [{"activity_id": 1, "confidence": 0.9}]
        features = self._prepare_features(user_features)
        predictions = self.model.predict(features)
        return [{"activity_id": 1, "predicted_type": str(predictions[0]), "confidence": 0.9}]

    def _prepare_features(self, user_features: dict) -> pd.DataFrame:
        activity_text = user_features.get("preferred_category", "sports")
        participants  = user_features.get("participants", 1)
        return pd.DataFrame([{
            "activity":     activity_text,
            "participants": participants
        }])

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