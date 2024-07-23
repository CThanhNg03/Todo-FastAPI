from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.exceptions import HTTPException
from starlette import status

from app.config.auth import verify_token

class FilterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("Authorization")
        
        if not request.url.path.startswith("/api/v1/admin"):
            response = await call_next(request)
            return response
        
        if not verify_token(token):
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": "You have to login first"}
            )
        
        _, role = verify_token(token)
        if role != "admin":
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": "You don't have permission to access this resource"}
            )
        
        response = await call_next(request)
        return response
        
        
        response = await call_next(request)