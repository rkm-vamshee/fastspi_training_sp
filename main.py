from fastapi import FastAPI 
from app.api import auth_api
# from core.database import Base,engine
# from models.user_model import User

# Base.metadata.create_all(bind=engine)

app = FastAPI(DEBUG=True)

@app.get("/")
def test():
    return "Hai"


app.include_router(auth_api.router, prefix="/api")

