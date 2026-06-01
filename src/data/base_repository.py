"""
src/data/base_repository.py
Temel Repository — tüm repository sınıfları buradan türeyecek
Repository Pattern: Business katmanı DB'ye direkt dokunmaz, buradan geçer
Sorumlu: Gurbet
"""

from sqlalchemy.orm import Session


class BaseRepository:
    def __init__(self, model, session: Session):
        self.model = model
        self.session = session

    def get_by_id(self, record_id: int):
        return self.session.get(self.model, record_id)

    def get_all(self):
        return self.session.query(self.model).all()

    def add(self, entity):
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def update(self, entity):
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def delete(self, record_id: int):
        entity = self.get_by_id(record_id)
        if entity:
            self.session.delete(entity)
            self.session.commit()
            return True
        return False