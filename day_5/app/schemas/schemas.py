from pydantic import BaseModel


class UserCreate(BaseModel):
    firstName:str
    lastName:str
    email:str
    mobileno:str
    hassedPassword:str
    
class LoginReq(BaseModel):
    email:str
    password:str
    
class SendOtpReq(BaseModel):
    email:str
class VerifyOtpReq(BaseModel):
    email:str
    otp:str
    