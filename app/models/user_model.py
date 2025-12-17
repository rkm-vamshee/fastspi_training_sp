from sqlalchemy import Boolean, Column, Integer, String
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
    mobileno = Column(String)
    email = Column(String, unique=True, nullable=False)
    hassedPassword = Column(String,nullable=False)
    isEmailVerified = Column(Boolean,default=False)



class EmailOtp(Base):
    __tablename__="email_otps"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    hassedOtp = Column(String,nullable=False)
    
    