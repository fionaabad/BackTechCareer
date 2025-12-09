from fastapi import HTTPException
from backend.api.v1.schemas.user_schemas import UserLogin
from backend.api.v1.schemas.user_schemas import UserRegister
from backend.db.queries.user_queries import LOGIN_QUERY
from backend.db.queries.user_queries import REGISTER_QUERY
from mysql.connector.errors import IntegrityError
from backend.db.connection import get_connection
from backend.core.security import verify_password
from backend.core.security import hash_password

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
        "user_id": user["idusers"]
    }
    
def register_user(data: UserRegister):
    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = hash_password(data.password)

    try:
        cursor.execute(
            REGISTER_QUERY,
            (data.email, hashed_password)
        )
        conn.commit()

    except IntegrityError:
        raise HTTPException(status_code=400, detail="El usuario ya existe.")

    return {"message": "Usuario registrado con éxito"}
