# from app.routers import auth_router, google_auth_router
# from app.core.auth.middlewares import SimpleMiddleware
from app.core.auth.middlewares import SimpleMiddleware
from app.routers import  auth_router
from fastapi import FastAPI 
from dotenv import load_dotenv
load_dotenv() 
# from app.routers import auth_router
# from app.routers.auth_router import router as authRouter

from app.core.database import Base,engine
from app.models.user_model import User
import os

from starlette.middleware.sessions import SessionMiddleware



Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY")
)

app.add_middleware(SimpleMiddleware)

@app.get("/")
def test():
    return "Hai"


app.include_router(auth_router.router, prefix="/api")
# app.include_router(google_auth_router.router, prefix="/api")

