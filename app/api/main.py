from fastapi import Depends, FastAPI, HTTPException

from core.database import Base,engine, getDB
from schemas.schemas import UserCreate
from models.user_model import User
from sqlalchemy.orm import Session
from passlib.context import CryptContext

Base.metadata.create_all(bind=engine)

bcrypt = CryptContext(schemes=['bcrypt'], deprecated="auto")

app = FastAPI()


@app.get("/")
def index():
    return "Working fine"



""" 
SIGNUP API


firstName
lastName
mobileno
email
hassedPassword=> 123=> skdfjlskdjfslkdf 

"""

@app.post("/signup")
def signup(user:UserCreate,db:Session=Depends(getDB) ):
    
    isUserExists = db.query(User).filter(User.email == user.email).first()
    if isUserExists:
        raise HTTPException(433, "Email already Exists")
    
    user.hassedPassword = bcrypt.hash( user.hassedPassword)
    
    newUser = User(firstName = user.firstName,
    lastName = user.lastName,
    mobileno = user.mobileno,
    email = user.email,
    hassedPassword = user.hassedPassword)
    
    db.add(newUser)
    db.commit()
    
    return user

