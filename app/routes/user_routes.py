from fastapi import APIRouter,  Request
from app.models.user_models import (
    RegisterRequest, LoginRequest, ChangePasswordRequest,
    ForgetPasswordRequest, ResetPasswordRequest,
    RegisterResponse,LoginResponse, GeneralResponse
    
)
from app.services.user_service import (
    register_user, login_user, change_password,
    forget_password, reset_password, logout_user
)

router = APIRouter()

@router.post("/register", response_model=RegisterResponse)
def register(request: RegisterRequest):
    return register_user(request)

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    return login_user(request)

@router.post("/change-password", response_model=GeneralResponse)
def change_pass(request: ChangePasswordRequest):
    return change_password(request)

@router.post("/forgot-password", response_model=GeneralResponse)
def forgot_pass(request: ForgetPasswordRequest):
    return forget_password(request)

@router.post("/reset-password", response_model=GeneralResponse)
def reset_pass(request: ResetPasswordRequest):
    return reset_password(request)

@router.post("/logout", response_model=GeneralResponse)
def logout(request: Request):
    return logout_user(request)
