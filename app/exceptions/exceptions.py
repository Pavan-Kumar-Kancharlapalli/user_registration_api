from fastapi import HTTPException, status

class UserAlreadyExistsException(HTTPException):
    def __init__(self, detail="User with this email or phone already exists."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class InvalidCredentialsException(HTTPException):
    def __init__(self, detail="Invalid email/phone or password."):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class TokenExpiredException(HTTPException):
    def __init__(self, detail="Token has expired."):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class UnauthorizedAccessException(HTTPException):
    def __init__(self, detail="You are not authorized to perform this action."):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class TooManyRequestsException(HTTPException):
    def __init__(self, detail="Too many requests. Please try again later."):
        super().__init__(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=detail)
