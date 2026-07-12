from sqlalchemy import Boolean, String

from sqlalchemy import Mapped, mapped_column

from database import Base

class TaskModel(Base): #this class is not a normal python class
#Task model inherited from base SO I SHOULD ADD THIS TO BASE.METADATA
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key = True, index = True)
    title: Mapped[str] = mapped_column(String(100), nullable = False)
    description: Mapped[str | None] = mapped_column(String(500), nullable = True)
    completed: Mapped[bool] = mapped_column(Boolean, default = False)

    # id = Column(Integer, primary_key = True, index = True)
    # title = Column(String, nullable = False)
    # description = Column(String, nullable = True)
    # Completed = Column(Boolean, default = False)
