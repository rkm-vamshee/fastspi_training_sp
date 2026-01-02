from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

class SimpleMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        print("➡️ Before request")
        # return await call_next(request)
        response = await call_next(request)
        print("⬅️ After response")
        return response
