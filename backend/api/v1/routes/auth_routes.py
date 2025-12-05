from fastapi import APIRouter
from backend.api.v1.schemas.user_schemas import UserLogin
from backend.api.v1.controllers.auth_controller import login_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(data: UserLogin):
    return login_user(data)
