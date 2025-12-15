from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.database import getDB
from app.schemas.schemas import LoginReq, UserCreate
from app.models.user_model import User
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError


bcrypt = CryptContext(schemes=['bcrypt'], deprecated="auto")


router = APIRouter(prefix="/auth", tags=['auth'])


@router.get("/")
def index():
    return "Working fine"


@router.post("/signup")
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


def createToken(id:int, name:str):
    data = {"id":id, "name":name}
    token = jwt.encode(data,"SECRET",algorithm="HS256")
    return token



@router.post('/login')
def login(req:LoginReq,db:Session=Depends(getDB) ):
    # Checking Email
    isUserExists = db.query(User).filter(User.email == req.email).first()
    if isUserExists is None:
        raise HTTPException(433, "Email and password invalid")
    # Compare Password
    isPasswordValid = bcrypt.verify(req.password, isUserExists.hassedPassword)
    print(isPasswordValid)
    if isPasswordValid==False:
        raise HTTPException(433, "Password invalid")
    return {"accessToken":createToken(isUserExists.id, isUserExists.firstName), "user":isUserExists}


@router.get('/public-data')
def getPublicData():
    return "Public data(Not Protected Data)"


""" How to protect """
security = HTTPBearer()

def getCurrentUser(credentials:HTTPAuthorizationCredentials=Depends(security)):
    token= credentials.credentials
    try:
        data = jwt.decode(token, "SECRET",algorithms=["HS256"])
        return data
        
    except JWTError:
        raise HTTPException(status_code=433, detail="User is invalid")
    
    
@router.get('/userdetails')
def getUserDetails(user=Depends(getCurrentUser)):
    return user
    

