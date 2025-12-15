from sqlalchemy import Column, Integer, String
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    """ 
    id
    firstName
    lastName
    mobileno
    email
    hassedPassword => Camel case
    
    """

    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String)
    lastName = Column(String)
    mobileno = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hassedPassword = Column(String,nullable=False)
