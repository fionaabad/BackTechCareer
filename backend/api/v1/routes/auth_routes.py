from fastapi import APIRouter
from api.v1.schemas.user_schemas import UserLogin
from api.v1.schemas.user_schemas import UserRegister
from api.v1.controllers.auth_controller import login_user
from api.v1.controllers.auth_controller import register_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(data: UserLogin):
    return login_user(data)

@router.post("/register")
def register(data: UserRegister):
    return register_user(data)
