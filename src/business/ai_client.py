"""
src/business/ai_client.py
AI API çağrısı — Strategy Pattern ile
Katman: Business
Sorumlu: Efe
"""

from abc import ABC, abstractmethod
import os


# ── Strategy arayüzü ──────────────────────────
class AIStrategy(ABC):
    @abstractmethod
    def generate_note(self, activity_name: str, user_preferences: dict) -> str:
        pass


# ── OpenAI stratejisi ─────────────────────────
class OpenAIStrategy(AIStrategy):
    def __init__(self):
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        except ImportError:
            raise ImportError("openai paketi kurulu değil: pip install openai")

    def generate_note(self, activity_name: str, user_preferences: dict) -> str:
        prompt = self._build_prompt(activity_name, user_preferences)
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()

    def _build_prompt(self, activity_name: str, prefs: dict) -> str:
        return (
            f"Kullanıcı profili: yaş={prefs.get('age')}, "
            f"bütçe={prefs.get('budget_range')} TL, "
            f"süre tercihi={prefs.get('max_duration_minutes')} dakika. "
            f"'{activity_name}' aktivitesi için kısa, motive edici bir öneri notu yaz. "
            f"Maksimum 2 cümle."
        )


# ── Gemini stratejisi ─────────────────────────
class GeminiStrategy(AIStrategy):
    def __init__(self):
        try:
            import google.generativeai as genai
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            self.model = genai.GenerativeModel("gemini-pro")
        except ImportError:
            raise ImportError("google-generativeai paketi kurulu değil")

    def generate_note(self, activity_name: str, user_preferences: dict) -> str:
        prompt = (
            f"Kullanıcı profili: yaş={user_preferences.get('age')}, "
            f"bütçe={user_preferences.get('budget_range')} TL. "
            f"'{activity_name}' için kısa motive edici not yaz. Maksimum 2 cümle."
        )
        response = self.model.generate_content(prompt)
        return response.text.strip()


# ── Context sınıfı ────────────────────────────
class AIClient:
    """
    Hangi AI servisinin kullanılacağını .env'den otomatik seçer.
    Business katmanı sadece bu sınıfı kullanır, stratejiyi bilmez.
    """
    def __init__(self):
        self.strategy = self._select_strategy()

    def _select_strategy(self):
        if os.getenv("OPENAI_API_KEY"):
            return OpenAIStrategy()
        elif os.getenv("GEMINI_API_KEY"):
            return GeminiStrategy()
        return None

    def generate_note(self, activity_name: str, user_preferences: dict) -> str:
        return self.strategy.generate_note(activity_name, user_preferences)