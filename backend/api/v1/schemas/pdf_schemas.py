from pydantic import BaseModel
from datetime import datetime
from typing import List

class PdfUploadResponse(BaseModel):
    message: str
    pdf_id: int
    filename: str

class PdfHistoryItem(BaseModel):
    idpdf: int
    filename: str
    uploaded_at: datetime
    processed: bool

class PdfHistoryResponse(BaseModel):
    user_id: int
    pdfs: List[PdfHistoryItem]
