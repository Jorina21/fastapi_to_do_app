from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
# from sqlalchemy.orm import sessionmaker, declarative_base



DATABASE_URL = "sqlite:///./task.db"

#main bridge betweeen python and the database
#created once on startup and handles traffic, connection, and file access
engine = create_engine(
    DATABASE_URL,
    connect_args = {"check_same_thread": False} #SQlite treadsafety rule: connection use the same tread as where they were created (uses fast api thread handling and not sqlite)
)

#Creates sessions (session factory)
SessionLocal = sessionmaker( #returns a class 
    #sessionlocal creates(session objects) 
    #sessionmaker inherits from session base class
    expire_on_commit = False,#makes returned objects easier to work with after commits()
    # autocommit = False, #wait until i say db.commit then save
    autoflush = False, #dont push pending changes to the db before every query
    bind = engine
)


# Base = declarative_base() #creates a parent class that is used in models
# returns a class like object 

class Base(DeclarativeBase):
    pass #instead of using prev use this

def get_db() -> Generator[Session: None, None]: #why 3 items in the list?
    db = SessionLocal()  #sessionmaker implements __call__ which allows it to be called like a function (factory)

    try:
        yield db
    
    finally:
        db.close()


