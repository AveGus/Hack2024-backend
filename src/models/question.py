from sqlalchemy import Column, Integer, String, ForeignKey

from services.database import Base


class question(Base):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True, autoincrement=True)
    case_id = Column(Integer, ForeignKey('case.id'))
    text = Column(String)