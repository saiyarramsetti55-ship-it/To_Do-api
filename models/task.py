from sqlalchemy import Column, Integer, String, Boolean
from database.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    priority = Column(String, default="medium")
    completed = Column(Boolean, default=False)
