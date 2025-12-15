from fastapi import HTTPException
<<<<<<< HEAD
from api.v1.schemas.user_schemas import UserLogin
from api.v1.schemas.user_schemas import UserRegister
from db.queries.user_queries import LOGIN_QUERY
from db.queries.user_queries import REGISTER_QUERY
from mysql.connector.errors import IntegrityError
from db.connection import get_connection
from core.security import verify_password
from core.security import hash_password
=======
from backend.api.v1.schemas.user_schemas import (
    UserLogin,
    UserRegister,
    UserUpdate,
    UpdatePassword
)
from backend.db.queries.user_queries import (
    LOGIN_QUERY,
    REGISTER_QUERY,
    UPDATE_USER_QUERY
)
from mysql.connector.errors import IntegrityError
from backend.db.connection import get_connection
from backend.core.security import verify_password, hash_password

>>>>>>> eaf515c83fe588bbe91d809a131cd579469262fa

def login_user(data: UserLogin):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(LOGIN_QUERY, (data.email,))
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=401, detail="Usuario no existe.")

    if not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta.")

    # devolver campos estándar para frontend
    return {
        "message": "Login exitoso",
        "user": {
            "id": user["idusers"],
            "email": user["email"],
            "name": user.get("name"),
            "avatar": user.get("avatar")
        }
    }


def register_user(data: UserRegister):
    conn = get_connection()
    cursor = conn.cursor()

    hashed = hash_password(data.password)

    cursor.execute(
        "INSERT INTO users (email, password, name, avatar) VALUES (%s, %s, %s, %s)",
        (data.email, hashed, data.name, data.avatar)
    )

    conn.commit()
    return {"message": "Usuario creado"}


def update_password_controller(data: UpdatePassword):
    conn = get_connection()
    cursor = conn.cursor()

    hashed = hash_password(data.new_password)

    cursor.execute(
        "UPDATE users SET password=%s WHERE idusers=%s",
        (hashed, data.user_id)
    )
    conn.commit()

    return {"message": "Contraseña actualizada"}


def update_user(user_id: int, data: UserUpdate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    new_email = data.email
    new_name = data.name
    new_avatar = data.avatar
    new_pass = hash_password(data.password) if data.password else None

    cursor.execute(
        UPDATE_USER_QUERY,
        (new_email, new_pass, new_name, new_avatar, user_id),
    )

    conn.commit()

    # obtener datos actualizados
    cursor.execute("SELECT idusers, email, name, avatar FROM users WHERE idusers=%s", (user_id,))
    updated = cursor.fetchone()

    return {
        "message": "Usuario actualizado correctamente",
        "updated_user": {
            "id": updated["idusers"],
            "email": updated["email"],
            "name": updated["name"],
            "avatar": updated["avatar"]
        }
    }
