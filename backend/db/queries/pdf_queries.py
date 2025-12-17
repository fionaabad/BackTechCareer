INSERT_PDF_QUERY = """
INSERT INTO users_pdfs (user_id, filename, storage_path, processed)
VALUES (%s, %s, %s, %s)
"""

GET_USER_PDFS_QUERY = """
SELECT idpdf, filename, uploaded_at, processed
FROM users_pdfs
WHERE user_id = %s
ORDER BY uploaded_at DESC
"""

MARK_PDF_PROCESSED_QUERY = """
UPDATE users_pdfs
SET processed = 1
WHERE idpdf = %s
"""

DELETE_PDF_QUERY = """
DELETE FROM users_pdfs
WHERE idpdf = %s AND user_id = %s
"""

GET_PDF_BY_ID_QUERY = """
SELECT file_path
FROM users_pdfs
WHERE idpdf = %s AND user_id = %s
"""
