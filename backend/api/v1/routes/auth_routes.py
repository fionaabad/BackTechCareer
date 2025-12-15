from fastapi import APIRouter
from backend.api.v1.schemas.user_schemas import UserLogin, UserRegister, UserUpdate, UpdatePassword
from backend.api.v1.controllers.auth_controller import (
    login_user,
    register_user,
    update_password_controller,
    update_user
)

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(data: UserLogin):
    return login_user(data)

@router.post("/register")
def register(data: UserRegister):
    return register_user(data)

@router.post("/update_password")
def update_password(data: UpdatePassword):
    return update_password_controller(data)

@router.put("/update/{user_id}")
def update(user_id: int, data: UserUpdate):
    return update_user(user_id, data)
