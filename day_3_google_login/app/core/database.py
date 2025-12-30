from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base


""" 
Url
engine
session
Base

function => injection

"""

# DB_URL="postgresql://username:password@localhost:5432/dbname"



DB_URL="postgresql://postgres:postgres@localhost:5432/myapp_db"

engine = create_engine(DB_URL)

SessionLocal=sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()


def getDB():
    db=SessionLocal()
    try:
        yield db 
    finally:
        db.close()