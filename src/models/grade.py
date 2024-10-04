from sqlalchemy import Column, Integer, ForeignKey

from services.database import Base


class grade(Base):
    __tablename__ = 'grade'
    id = Column(Integer, primary_key=True)
    command_id = Column(Integer, ForeignKey('command.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    question_id = Column(Integer, ForeignKey('question.id'))
    score = Column(Integer)