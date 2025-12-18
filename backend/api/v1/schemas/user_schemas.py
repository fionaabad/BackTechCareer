from pydantic import BaseModel, EmailStr
from typing import Optional, Literal


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    confirm_password: str
    role: Literal["particular", "empresa"]


class UpdatePassword(BaseModel):
    user_id: int
    new_password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
