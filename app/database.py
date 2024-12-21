from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name }"

# creates a connection between your application and the database.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# create a configured database session class (SessionLocal), which can be used to interact with the database.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# provides a base class (Base) for all your ORM models. ORM models define how Python classes correspond to database tables.
Base = declarative_base()

# function to create db session and then close it once done
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()