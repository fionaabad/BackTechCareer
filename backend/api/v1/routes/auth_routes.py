from fastapi import APIRouter, status
from backend.api.v1.schemas.user_schemas import (
    UserLogin,
    UserRegister,
    UserUpdate,
    UpdatePassword
)
from backend.api.v1.controllers.auth_controller import (
    login_user,
    register_user,
    update_password_controller,
    update_user
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post(
    "/login",
    status_code=status.HTTP_200_OK
)
def login(data: UserLogin):
    return login_user(data)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED
)
def register(data: UserRegister):
    return register_user(data)


@router.post(
    "/update_password",
    status_code=status.HTTP_200_OK
)
def update_password(data: UpdatePassword):
    return update_password_controller(data)


@router.put(
    "/update/{user_id}",
    status_code=status.HTTP_200_OK
)
def update(user_id: int, data: UserUpdate):
    return update_user(user_id, data)
