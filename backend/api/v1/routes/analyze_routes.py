# backend/api/v1/routes/analyze_routes.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

from backend.api.v1.controllers.analyze_controller import analyze_cv
from backend.utils.extract_text_from_pdf import extract_text_from_pdf

router = APIRouter()


# =========================
# MODELO TEXTO (API interna / tests)
# =========================
class CVRequest(BaseModel):
    cv_text: str


@router.post("/analyze-cv")
def analyze_from_text(request: CVRequest):
    """
    Endpoint técnico.
    Analiza un CV a partir de texto plano.
    Útil para pruebas y llamadas internas.
    """
    if not request.cv_text or len(request.cv_text.strip()) < 100:
        raise HTTPException(
            status_code=400,
            detail="Texto de CV insuficiente"
        )

    return analyze_cv(request.cv_text)


# =========================
# MODELO PDF (ENDPOINT PRODUCTO)
# =========================
@router.post("/analyze-cv/pdf")
async def analyze_from_pdf(file: UploadFile = File(...)):
    """
    Endpoint de producto.
    Recibe un PDF, extrae texto y ejecuta el análisis completo.
    """

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Solo se permiten archivos PDF"
        )

    pdf_bytes = await file.read()

    if not pdf_bytes:
        raise HTTPException(
            status_code=400,
            detail="Archivo PDF vacío"
        )

    cv_text = extract_text_from_pdf(pdf_bytes)

    if not cv_text or len(cv_text.strip()) < 100:
        raise HTTPException(
            status_code=400,
            detail="No se pudo extraer texto válido del CV"
        )

    result = analyze_cv(cv_text)

    return {
        "status": "ok",
        "filename": file.filename,
        **result
    }
