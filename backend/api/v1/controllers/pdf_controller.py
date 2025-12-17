from backend.db.connection import get_connection


def get_pdf_history(user_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT idpdf, filename, uploaded_at, processed
        FROM users_pdfs
        WHERE user_id = %s
        ORDER BY uploaded_at DESC
        """,
        (user_id,)
    )

    pdfs = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "user_id": user_id,
        "pdfs": pdfs
    }


def delete_pdf(pdf_id: int, user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM users_pdfs WHERE idpdf = %s AND user_id = %s",
        (pdf_id, user_id)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return {"deleted": True}
