from fastapi import HTTPException
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


def login_user(data: UserLogin):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(LOGIN_QUERY, (data.email,))
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=401, detail="Usuario no existe.")

    if not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta.")

    return {
        "message": "Login exitoso",
        "user": {
            "id": user["idusers"],
            "email": user["email"],
            "name": user.get("name"),
        }
    }


def register_user(data: UserRegister):
    # 1️⃣ Validación de contraseñas
    if data.password != data.confirm_password:
        raise HTTPException(
            status_code=400,
            detail="Las contraseñas no coinciden"
        )

    conn = get_connection()
    cursor = conn.cursor()

    # 2️⃣ Hasheamos contraseña
    hashed_password = hash_password(data.password)

    try:
        # 3️⃣ Insert usuario
        cursor.execute(
            REGISTER_QUERY,
            (
                data.email,
                hashed_password,
                data.name,
            )
        )
        conn.commit()

    except IntegrityError:
        # Email duplicado
        raise HTTPException(
            status_code=409,
            detail="El email ya está registrado"
        )

    finally:
        cursor.close()
        conn.close()

    # 4️⃣ Respuesta limpia para el frontend
    return {
        "message": "Usuario creado correctamente",
        "user": {
            "email": data.email,
            "name": data.name,
        }
    }


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
    new_pass = hash_password(data.password) if data.password else None

    cursor.execute(
        UPDATE_USER_QUERY,
        (new_email, new_pass, new_name, user_id),
    )

    conn.commit()

    cursor.execute(
        "SELECT idusers, email, name FROM users WHERE idusers=%s",
        (user_id,)
    )
    updated = cursor.fetchone()

    return {
        "message": "Usuario actualizado correctamente",
        "updated_user": {
            "id": updated["idusers"],
            "email": updated["email"],
            "name": updated["name"],
        }
    }
