from pydantic import BaseModel


class UserCreate(BaseModel):
    firstName:str
    lastName:str
    email:str
    mobileno:str
    hassedPassword:str
    