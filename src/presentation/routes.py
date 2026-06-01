"""
src/presentation/routes.py
Flask route'ları — sadece servis katmanını çağırır
Katman: Presentation
Sorumlu: Lizge
KURAL: Bu katman DB'ye ve modele direkt dokunmaz!
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from src.data.database import SessionLocal
from src.data.user_repository import UserRepository
from src.data.activity_repository import ActivityRepository
from src.business.activity_service import ActivityService
from src.business.recommendation_engine import RecommendationEngine
from src.business.ai_client import AIClient

bp = Blueprint("main", __name__)


def get_service():
    """Her request'te servis nesnesi oluşturur."""
    db = SessionLocal()
    activity_repo = ActivityRepository(db)
    user_repo     = UserRepository(db)
    engine        = RecommendationEngine()
    ai_client     = AIClient()
    return ActivityService(activity_repo, user_repo, engine, ai_client)


# ── Ana sayfa ──────────────────────────────────
@bp.route("/")
def index():
    return render_template("index.html")


# ── Kayıt ──────────────────────────────────────
@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email    = request.form.get("email")
        password = request.form.get("password")

        if not username or not email or not password:
            flash("Tüm alanları doldurun.", "error")
            return render_template("register.html")

        db        = SessionLocal()
        user_repo = UserRepository(db)

        if user_repo.get_by_email(email):
            flash("Bu e-posta zaten kayıtlı.", "error")
            return render_template("register.html")

        from src.data.models import User
        import hashlib
        hashed = hashlib.sha256(password.encode()).hexdigest()
        user = User(username=username, email=email, password=hashed)
        user_repo.add(user)

        flash("Kayıt başarılı! Giriş yapabilirsiniz.", "success")
        return redirect(url_for("main.login"))

    return render_template("register.html")


# ── Giriş ──────────────────────────────────────
@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email    = request.form.get("email")
        password = request.form.get("password")

        db        = SessionLocal()
        user_repo = UserRepository(db)
        user      = user_repo.get_by_email(email)

        import hashlib
        hashed = hashlib.sha256(password.encode()).hexdigest()

        if not user or user.password != hashed:
            flash("E-posta veya şifre hatalı.", "error")
            return render_template("login.html")

        session["user_id"]   = user.id
        session["username"]  = user.username
        return redirect(url_for("main.dashboard"))

    return render_template("login.html")


# ── Çıkış ──────────────────────────────────────
@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.index"))


# ── Dashboard ──────────────────────────────────
@bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    service     = get_service()
    suggestions = service.get_recommendations(session["user_id"])
    return render_template("dashboard.html",
                           username=session["username"],
                           suggestions=suggestions)


# ── Tercihler ──────────────────────────────────
@bp.route("/preferences", methods=["GET", "POST"])
def preferences():
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    if request.method == "POST":
        from src.data.models import UserPreference, ActivityCategory, DifficultyLevel
        db        = SessionLocal()
        user_repo = UserRepository(db)
        user      = user_repo.get_by_id(session["user_id"])

        pref = user.preferences or UserPreference(user_id=user.id)
        pref.age                  = int(request.form.get("age", 25))
        pref.preferred_category   = ActivityCategory(request.form.get("category", "sports"))
        pref.max_duration_minutes = int(request.form.get("duration", 60))
        pref.preferred_difficulty = DifficultyLevel(request.form.get("difficulty", "medium"))
        pref.indoor_preference    = request.form.get("indoor") == "true"
        pref.budget_range         = float(request.form.get("budget", 100.0))

        if not user.preferences:
            db.add(pref)
        db.commit()

        flash("Tercihler kaydedildi!", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("preferences.html")


# ── Aktiviteler ────────────────────────────────
@bp.route("/activities")
def activities():
    service    = get_service()
    activities = service.get_all_activities()
    return render_template("activities.html", activities=activities)