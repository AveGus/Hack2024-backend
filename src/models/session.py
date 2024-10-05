from datetime import datetime

from sqlalchemy import Integer, Column, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship

from models import Command
from services.database import Base


class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    command_id = Column(Integer, ForeignKey("command.id"), nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    status = Column(String, default="awaiting")  # Возможные статусы: 'awaiting', 'performing', 'not_evaluated', 'evaluated'
    duration = Column(Integer, default=600)
    command = relationship(Command, lazy="selectin")
