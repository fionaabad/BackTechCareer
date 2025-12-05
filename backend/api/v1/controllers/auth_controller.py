from fastapi import HTTPException
from backend.api.v1.schemas.user_schemas import UserLogin
from backend.db.connection import get_connection
from backend.db.queries.user_queries import LOGIN_QUERY
from backend.core.security import verify_password

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
