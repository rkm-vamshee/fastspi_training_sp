# from app.routers import auth_router, google_auth_router
from app.routers import  google_auth_router
from fastapi import FastAPI 
# from app.routers import auth_router
# from app.routers.auth_router import router as authRouter

from app.core.database import Base,engine
from app.models.user_model import User

Base.metadata.create_all(bind=engine)

from dotenv import load_dotenv
import os
from starlette.middleware.sessions import SessionMiddleware


load_dotenv() 

app = FastAPI()


app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY")
)

@app.get("/")
def test():
    return "Hai"


# app.include_router(auth_router, prefix="/api")
app.include_router(google_auth_router.router, prefix="/api")

