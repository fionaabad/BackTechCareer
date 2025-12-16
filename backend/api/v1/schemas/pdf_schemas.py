from pydantic import BaseModel
from typing import Optional


class PdfCreate(BaseModel):
    user_id: int
    filename: str
    pdf_data: str  # base64 del PDF


class PdfOut(BaseModel):
    idpdf: int
    user_id: int
    filename: str
    created_at: str
