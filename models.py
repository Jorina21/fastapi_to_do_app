from sqlalchemy import Boolean, Column, Integer, String

from database import Base

class TaskModel(Base): #this class is not a normal python class
#Task model inherited from base SO I SHOULD ADD THIS TO BASE.METADATA
    __tablename__ = "tasks"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, nullable = False)
    description = Column(String, nullable = True)
    Completed = Column(Boolean, default = False)
