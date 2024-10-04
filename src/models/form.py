from sqlalchemy import Column, Integer

from services.database import Base


class Form(Base):
    __tablename__ = 'form'
    id = Column(Integer, primary_key=True, autoincrement=True)


