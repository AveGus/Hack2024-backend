from sqlalchemy import Column, Integer, String, ForeignKey, VARCHAR
from sqlalchemy.orm import relationship

from models import Case
from services.database import Base


class Command(Base):
    __tablename__ = 'command'
    id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String)
    case_id = Column(Integer, ForeignKey('case.id'))
    status = Column(VARCHAR, default='Ожидают', nullable=True)
    case = relationship(Case, lazy='selectin')
