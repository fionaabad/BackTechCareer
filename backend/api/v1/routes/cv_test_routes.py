from fastapi import APIRouter, UploadFile, File, HTTPException

from backend.utils.extract_text_from_pdf import extract_text_from_pdf
from backend.services.cv_analysis_orchestrator import analyze_cv_orchestrator

router = APIRouter(tags=["CV Test"])


@router.post("/cv/test-analyze")
async def test_analyze_cv(file: UploadFile = File(...)):

    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Solo PDFs")

    pdf_bytes = await file.read()
    text = extract_text_from_pdf(pdf_bytes)

    if not text or len(text.strip()) < 100:
        raise HTTPException(
            status_code=400,
            detail="Texto extraído insuficiente"
        )

    salary_params = {
        "country": "ES",
        "company_size": "M",
        "employment_type": "FT",
        "work_year": 2025,
        "remote_ratio": 50,
    }

    result = analyze_cv_orchestrator(text, salary_params)

    return {
        "status": "ok",
        "filename": file.filename,
        **result
    }
