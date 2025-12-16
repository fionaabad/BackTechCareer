CREATE_PDF_QUERY = """
    INSERT INTO user_pdfs (user_id, filename, pdf_data)
    VALUES (%s, %s, %s)
"""

GET_USER_PDFS_QUERY = """
    SELECT idpdf, user_id, filename, created_at
    FROM user_pdfs
    WHERE user_id = %s
    ORDER BY created_at DESC
"""

DELETE_PDF_QUERY = """
    DELETE FROM user_pdfs
    WHERE idpdf = %s
"""
