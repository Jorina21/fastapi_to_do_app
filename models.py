from sqlalchemy import Boolean, Column, Integer, String

from database import Base

class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, Primary_key = True, index = True)
    title = Column(String, nullable = False)
    description = Column(String, nullable = True)
    Completed = Column(Boolean, default = False)
