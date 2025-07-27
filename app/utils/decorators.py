from functools import wraps
from fastapi import Request, HTTPException
from app.utils.jwt_utils import decode_token
from starlette.status import HTTP_401_UNAUTHORIZED

def login_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get('request') or args[0]
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Authorization header missing")
        token = auth_header.replace("Bearer ", "")
        try:
            payload = decode_token(token)
            request.state.user = payload  # store user info
        except Exception as e:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
        return await func(*args, **kwargs)
    return wrapper
