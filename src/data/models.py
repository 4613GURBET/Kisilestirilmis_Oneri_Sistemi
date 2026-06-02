from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean,
    DateTime, ForeignKey, Table, Text, Enum
)
from sqlalchemy.orm import relationship, DeclarativeBase
import enum


class Base(DeclarativeBase):
    pass


class ActivityCategory(enum.Enum):
    SPORTS      = "sports"
    ART         = "art"
    MUSIC       = "music"
    OUTDOOR     = "outdoor"
    INDOOR      = "indoor"
    SOCIAL      = "social"
    EDUCATIONAL = "educational"
    WELLNESS    = "wellness"


class DifficultyLevel(enum.Enum):
    EASY   = "easy"
    MEDIUM = "medium"
    HARD   = "hard"


class PlanStatus(enum.Enum):
    PENDING   = "pending"
    ACTIVE    = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


user_hobbies = Table(
    "user_hobbies",
    Base.metadata,
    Column("user_id",  Integer, ForeignKey("users.id"),   primary_key=True),
    Column("hobby_id", Integer, ForeignKey("hobbies.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id         = Column(Integer, primary_key=True, autoincrement=True)
    username   = Column(String(50),  unique=True, nullable=False)
    email      = Column(String(120), unique=True, nullable=False)
    password   = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active  = Column(Boolean, default=True)

    preferences = relationship("UserPreference", back_populates="user", uselist=False, cascade="all, delete-orphan")
    daily_plans = relationship("DailyPlan", back_populates="user", cascade="all, delete-orphan")
    hobbies     = relationship("Hobby", secondary=user_hobbies, back_populates="users")


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id                   = Column(Integer, primary_key=True, autoincrement=True)
    user_id              = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    age                  = Column(Integer)
    preferred_category   = Column(Enum(ActivityCategory))
    max_duration_minutes = Column(Integer)
    preferred_difficulty = Column(Enum(DifficultyLevel))
    indoor_preference    = Column(Boolean, default=True)
    budget_range         = Column(Float)
    updated_at           = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="preferences")


class Activity(Base):
    __tablename__ = "activities"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    name        = Column(String(100), nullable=False)
    description = Column(Text)
    category    = Column(Enum(ActivityCategory), nullable=False)
    difficulty  = Column(Enum(DifficultyLevel),  nullable=False)
    duration    = Column(Integer)
    is_indoor   = Column(Boolean, default=True)
    min_budget  = Column(Float, default=0.0)
    max_budget  = Column(Float)
    is_active   = Column(Boolean, default=True)
    created_at  = Column(DateTime, default=datetime.utcnow)

    daily_plans = relationship("DailyPlan", back_populates="activity")


class Hobby(Base):
    __tablename__ = "hobbies"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    name        = Column(String(80), unique=True, nullable=False)
    category    = Column(Enum(ActivityCategory))
    description = Column(Text)

    users = relationship("User", secondary=user_hobbies, back_populates="hobbies")


class DailyPlan(Base):
    __tablename__ = "daily_plans"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    user_id     = Column(Integer, ForeignKey("users.id"),      nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    plan_date   = Column(DateTime, nullable=False)
    status      = Column(Enum(PlanStatus), default=PlanStatus.PENDING)
    ai_note     = Column(Text)
    rating      = Column(Integer)
    created_at  = Column(DateTime, default=datetime.utcnow)
    updated_at  = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user     = relationship("User",     back_populates="daily_plans")
    activity = relationship("Activity", back_populates="daily_plans")