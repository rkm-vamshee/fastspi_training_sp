from fastapi import APIRouter
from authlib.integrations.starlette_client import OAuth


""" 

pip install authlib

Useful Link:
https://youtu.be/5h63AfcVerM?t=1335

Other Link:
https://www.youtube.com/watch?v=4ExQYRCwbzw


"""
router = APIRouter()
oauth = OAuth()

oauth.register(
    name="google",
    client_id="GOOGLE_CLIENT_ID",
    client_secret="GOOGLE_CLIENT_SECRET",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

@router.get("/login/google")
async def google_login(request):
    return await oauth.google.authorize_redirect(
        request, "http://localhost:8000/auth/google/callback"
    )


@router.get("/auth/google/callback")
async def google_callback(request):
    token = await oauth.google.authorize_access_token(request)
    user = token["userinfo"]

    email = user["email"]
    name = user["name"]

    # AUTO CREATE USER
    # db_user = get_or_create_user(email, "google", name)

    # jwt_token = create_token({"email": email})
    return {"access_token": "jwt_token"}
