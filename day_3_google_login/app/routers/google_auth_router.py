import os
from fastapi import APIRouter, Depends, HTTPException
from authlib.integrations.starlette_client import OAuth
from sqlalchemy.orm import Session
from app.core.database import getDB
from app.models.user_model import User
from jose import jwt, JWTError
from passlib.context import CryptContext

""" 
pip install authlib

Useful Link:
https://youtu.be/5h63AfcVerM?t=1335

Other Link:
https://www.youtube.com/watch?v=4ExQYRCwbzw

"""

router = APIRouter()
oauth = OAuth()
bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


oauth.register(
    name="google",
    client_id= os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret= os.environ.get("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

@router.get("/login/google")
async def google_login(request):
    return await oauth.google.authorize_redirect(
        request, os.environ.get("GOOGLE_REDIRECT_URI")
    )


@router.get("/google/callback")
async def google_callback(request,db: Session = Depends(getDB)):
    token = await oauth.google.authorize_access_token(request)
    user = token["userinfo"]

    email = user["email"]
    name = user["name"]
    
    isUserExists = db.query(User).filter(User.email == email).first()
    if isUserExists:
        raise HTTPException(433, "Email already Exists")

    newUser = User(
        firstName=name,
        lastName=name,
        mobileno="",
        email=email,
        hassedPassword=bcrypt.hash("123")
    )

    db.add(newUser)
    db.commit()
    db.refresh(newUser) 
    
    return {"message": "user created successfully", "userDetails":newUser}
