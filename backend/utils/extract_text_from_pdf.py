# backend/utils/extract_text_from_pdf.py

import fitz  # PyMuPDF
from io import BytesIO


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extrae texto limpio de un PDF usando PyMuPDF.
    Devuelve un string con el texto concatenado.
    """

    text_parts = []

    try:
        with fitz.open(stream=BytesIO(pdf_bytes), filetype="pdf") as doc:
            for page in doc:
                page_text = page.get_text("text")
                if page_text:
                    text_parts.append(page_text)

    except Exception as e:
        print(f"[PDF ERROR] {e}")
        return ""

    return "\n".join(text_parts).strip()
