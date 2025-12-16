from fastapi import HTTPException
from backend.db.connection import get_connection
from backend.db.queries.pdf_queries import (
    CREATE_PDF_QUERY,
    GET_USER_PDFS_QUERY,
    DELETE_PDF_QUERY
)
from backend.api.v1.schemas.pdf_schemas import PdfCreate


def upload_pdf(data: PdfCreate):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        CREATE_PDF_QUERY,
        (data.user_id, data.filename, data.pdf_data)
    )
    conn.commit()

    return {"message": "PDF guardado correctamente"}


def get_user_pdfs(user_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(GET_USER_PDFS_QUERY, (user_id,))
    pdfs = cursor.fetchall()

    return {"pdfs": pdfs}


def delete_pdf(pdf_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(DELETE_PDF_QUERY, (pdf_id,))
    conn.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="PDF no encontrado")

    return {"message": "PDF eliminado correctamente"}
