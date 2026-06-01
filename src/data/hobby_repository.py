"""
src/data/hobby_repository.py
Sorumlu: Gurbet
"""

from sqlalchemy.orm import Session
from src.data.base_repository import BaseRepository
from src.data.models import Hobby, User


class HobbyRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(Hobby, session)

    def get_by_name(self, name: str):
        return self.session.query(Hobby).filter(Hobby.name == name).first()

    def get_user_hobbies(self, user_id: int):
        user = self.session.get(User, user_id)
        return user.hobbies if user else []

    def add_hobby_to_user(self, user_id: int, hobby_id: int):
        user  = self.session.get(User, user_id)
        hobby = self.session.get(Hobby, hobby_id)
        if user and hobby and hobby not in user.hobbies:
            user.hobbies.append(hobby)
            self.session.commit()
            return True
        return False