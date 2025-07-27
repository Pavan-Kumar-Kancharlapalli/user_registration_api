from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class RegisterRequest(BaseModel):
    username: str = Field(..., description="Email or phone number")
    password: str = Field(..., min_length=8, max_length=20)
    first_name: str
    last_name: str
    address: str


class RegisterResponse(BaseModel):
    message: str
    email_or_phone: str
    token: str



class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    message: str
    token: str



class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str


class ForgetPasswordRequest(BaseModel):
    username: str


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


class GeneralResponse(BaseModel):
    message: str

