"""
src/data/user_repository.py
Sorumlu: Gurbet
"""

from sqlalchemy.orm import Session
from src.data.base_repository import BaseRepository
from src.data.models import User


class UserRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(User, session)

    def get_by_email(self, email: str):
        return self.session.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str):
        return self.session.query(User).filter(User.username == username).first()

    def get_active_users(self):
        return self.session.query(User).filter(User.is_active == True).all()