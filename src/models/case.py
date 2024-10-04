from sqlalchemy import Column, String, Integer

from services.database import Base


class Case(Base):
    __tablename__ = 'case'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)