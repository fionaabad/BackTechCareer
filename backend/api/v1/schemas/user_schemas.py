from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    email: str
    password: str


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    avatar: str | None = None


class UpdatePassword(BaseModel):
    user_id: int
    new_password: str


class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None
    avatar: str | None = None
