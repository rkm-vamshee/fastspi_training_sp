from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError


security = HTTPBearer()


def getCurrentUser(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        data = jwt.decode(token, "SECRET", algorithms=["HS256"])
        return data

    except JWTError:
        raise HTTPException(status_code=433, detail="User is invalid")