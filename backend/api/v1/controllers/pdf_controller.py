import os
import uuid
from fastapi import UploadFile, HTTPException
from backend.db.connection import get_connection
from backend.db.queries.pdf_queries import (
    INSERT_PDF_QUERY,
    GET_USER_PDFS_QUERY,
    GET_PDF_BY_ID_QUERY,
    DELETE_PDF_QUERY
)

# Ruta base donde se guardan los CVs
UPLOAD_BASE_PATH = "backend/uploads/cvs"


def upload_pdf(file: UploadFile, user_id: int):
    # 1. Validar tipo de archivo
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")

    # 2. Crear carpeta del usuario si no existe
    user_folder = os.path.join(UPLOAD_BASE_PATH, f"user_{user_id}")
    os.makedirs(user_folder, exist_ok=True)

    # 3. Generar nombre único
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(user_folder, unique_filename)

    # 4. Guardar archivo en disco
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # 5. Guardar metadata en la BD
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        INSERT_PDF_QUERY,
        (user_id, unique_filename, file_path, 0)
    )
    conn.commit()

    pdf_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return {
        "message": "PDF subido correctamente",
        "pdf_id": pdf_id,
        "filename": unique_filename
    }


def get_pdf_history(user_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(GET_USER_PDFS_QUERY, (user_id,))
    pdfs = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "user_id": user_id,
        "pdfs": pdfs
    }


def delete_pdf(pdf_id: int, user_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # 1. Comprobar que el PDF existe y pertenece al usuario
    cursor.execute(GET_PDF_BY_ID_QUERY, (pdf_id, user_id))
    pdf = cursor.fetchone()

    if not pdf:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="PDF no encontrado")

    file_path = pdf["file_path"]

    # 2. Borrar archivo del sistema
    if os.path.exists(file_path):
        os.remove(file_path)

    # 3. Borrar registro de la base de datos
    cursor.execute(DELETE_PDF_QUERY, (pdf_id, user_id))
    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "PDF eliminado correctamente"
    }
