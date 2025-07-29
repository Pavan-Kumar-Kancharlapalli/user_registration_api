from fastapi import HTTPException, Request
from app.models.user_models import (
    RegisterRequest, RegisterResponse,
    LoginRequest, LoginResponse,
    ForgetPasswordRequest, ResetPasswordRequest,
    GeneralResponse
)
from app.data.db import user_collection
from app.utils.password_utils import hash_password, verify_password
from app.utils.jwt_utils import create_access_token,verify_token
from app.utils.logger import logger
from bson.objectid import ObjectId

def register_user(request: RegisterRequest) -> RegisterResponse:
    if user_collection.find_one({"username": request.username}):
        logger.warning(f"User already exists: {request.username}")
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(request.password)

    user_data = {
        "username": request.username,
        "password": hashed_password,
        "first_name": request.first_name,
        "last_name": request.last_name,
        "address": request.address,
    }

    user_collection.insert_one(user_data)

    access_token = create_access_token({"sub": request.username})
    logger.info(f"User registered: {request.username}")

    return RegisterResponse(
        message="Registration successful",
        email_or_phone=request.username,
        token=access_token
    )

def login_user(request: LoginRequest) -> LoginResponse:
    user = user_collection.find_one({"username": request.username})
    if not user or not verify_password(request.password, user["password"]):
        logger.warning(f"Invalid credentials for user: {request.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": request.username})
    logger.info(f"User logged in: {request.username}")

    return LoginResponse(
        message="Login successful",
        token=access_token
    )

def forget_password(request: ForgetPasswordRequest) -> GeneralResponse:
    user = user_collection.find_one({"username": request.username})
    if not user:
        logger.warning(f"User not found for forget password: {request.username}")
        raise HTTPException(status_code=404, detail="User not found")

    token = create_access_token({"sub": request.username})
    logger.info(f"Password reset token generated for: {request.username}")

    # In a real app, email or SMS this token.
    return GeneralResponse(message=f"Reset token: {token}")

def reset_password(request: ResetPasswordRequest) -> GeneralResponse:
    payload = verify_token(request.token)
    username = payload.get("sub")
    if not username:
        logger.warning("Invalid token used for password reset")
        raise HTTPException(status_code=401, detail="Invalid token")

    hashed_new_pw = hash_password(request.new_password)

    result = user_collection.update_one(
        {"username": username},
        {"$set": {"password": hashed_new_pw}}
    )

    if result.modified_count == 0:
        logger.warning(f"Password reset failed for user: {username}")
        raise HTTPException(status_code=400, detail="Password reset failed")

    logger.info(f"Password reset successful for user: {username}")
    return GeneralResponse(message="Password reset successful")

def logout_user(request: Request) -> GeneralResponse:
    # In real scenarios, you'd handle blacklisting the token or managing state
    logger.info("User logged out.")
    return GeneralResponse(message="Logout successful")
