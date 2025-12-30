import email
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.database import getDB
from app.schemas.schemas import LoginReq, SendOtpReq, UserCreate, VerifyOtpReq
from app.models.user_model import EmailOtp, User
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError

from app.utils.otp_utils import generateOtp, sendEmailForOtp


bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


router = APIRouter(tags=["Authentication"])


@router.get("/")
def index():
    return "Working fine"


@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(getDB)):

    isUserExists = db.query(User).filter(User.email == user.email).first()
    if isUserExists:
        raise HTTPException(433, "Email already Exists")

    user.hassedPassword = bcrypt.hash(user.hassedPassword)

    newUser = User(
        firstName=user.firstName,
        lastName=user.lastName,
        mobileno=user.mobileno,
        email=user.email,
        hassedPassword=user.hassedPassword,
    )

    db.add(newUser)
    db.commit()

    return {"message":"Your signup is successful."}


def createToken(id: int, name: str):
    data = {"id": id, "name": name}
    token = jwt.encode(data, "SECRET", algorithm="HS256")
    return token


@router.post("/login")
def login(req: LoginReq, db: Session = Depends(getDB)):
    # Checking Email
    isUserExists = db.query(User).filter(User.email == req.email).first()
    if isUserExists is None:
        raise HTTPException(433, "Email and password invalid")
    if isUserExists.isEmailVerified:
        raise HTTPException(433, "Email is not verified")
    
    # Compare Password
    isPasswordValid = bcrypt.verify(req.password, isUserExists.hassedPassword)
    
    print(isPasswordValid)
    if isPasswordValid == False:
        raise HTTPException(433, "Password invalid")
    
    return {
        "accessToken": createToken(isUserExists.id, isUserExists.firstName),
        "user": isUserExists,
    }


@router.get("/public-data")
def getPublicData():
    return "Public data(Not Protected Data)"


""" How to protect """
security = HTTPBearer()


def getCurrentUser(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        data = jwt.decode(token, "SECRET", algorithms=["HS256"])
        return data

    except JWTError:
        raise HTTPException(status_code=433, detail="User is invalid")


@router.get("/userdetails")
def getUserDetails(user=Depends(getCurrentUser)):
    return user


""" For Email OTPS """


@router.post("/send-otp")
def sendOtp(req: SendOtpReq, db: Session = Depends(getDB)):
    isUserExists = db.query(User).filter(User.email == req.email).first()
    
    
    if isUserExists is None:
        raise HTTPException(433, "Email invalid")
    
    if isUserExists.isEmailVerified:
        raise HTTPException(433, "Email is already verified")

    # otpGenerate
    otp = generateOtp()

    # storeInthetable
    emailOtp = EmailOtp(email=req.email, hassedOtp=otp)
    db.add(emailOtp)
    db.commit()
    # send to email
    sendEmailForOtp(req.email,otp)
    
    return {"message":"OTP sent successfully"}



@router.post("/verify-otp")
def verifyOtp(req: VerifyOtpReq, db: Session = Depends(getDB)):
    
    isEmailOtpPresent = db.query(EmailOtp).filter(EmailOtp.email==req.email).first()
    if isEmailOtpPresent is None:
        raise HTTPException(433, "Email invalid") 
    
    if req.otp == isEmailOtpPresent.hassedOtp:
        isUserExists = db.query(User).filter(User.email == req.email).first()
        isUserExists.isEmailVerified = True
        db.add(isUserExists)
        db.commit()
        return {"message":"Email Verified"}
    
    raise HTTPException(433, "OTP invalid") 