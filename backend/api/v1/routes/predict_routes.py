from fastapi import APIRouter, UploadFile, File
from backend.api.v1.controllers.predict_controller import (
    extract_text_from_pdf,
    predict_text
)

router = APIRouter(tags=["Prediction"])

@router.post("/predict_pdf")
async def predict_pdf(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    text = extract_text_from_pdf(pdf_bytes)

    if not text.strip():
        return {"error": "El PDF no contiene texto legible."}

    result = predict_text(text)

    return {
        "filename": file.filename,
        "texto_extraido": text[:15000],
        "prediccion": result["prediccion"],
        "top3": result["top3"],
        "probabilidades": result["probabilidades"],
    }
