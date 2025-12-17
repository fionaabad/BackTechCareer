from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.api.v1.controllers.analyze_controller import analyze_cv
from backend.utils.extract_text_from_pdf import extract_text_from_pdf

router = APIRouter()


@router.post("/analyze-cv/pdf")
async def analyze_from_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Solo PDFs")

    pdf_bytes = await file.read()
    if not pdf_bytes:
        raise HTTPException(status_code=400, detail="PDF vacío")

    cv_text = extract_text_from_pdf(pdf_bytes)
    if not cv_text or len(cv_text.strip()) < 100:
        raise HTTPException(status_code=400, detail="Texto insuficiente")

    result = analyze_cv(cv_text)

    return result
