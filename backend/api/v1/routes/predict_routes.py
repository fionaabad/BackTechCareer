from fastapi import APIRouter, UploadFile, File, HTTPException

from backend.api.v1.controllers.predict_controller import (
    extract_text_from_pdf,
    predict_text,
)

from backend.api.v1.controllers.seniority_controller import (
    predict_seniority_from_text,
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


@router.post("/predict_seniority")
async def predict_seniority(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    text = extract_text_from_pdf(pdf_bytes)

    if not text.strip():
        return {"error": "El PDF no contiene texto legible."}

    try:
        seniority = predict_seniority_from_text(text)
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error prediciendo seniority: {str(e)}")

    return {"filename": file.filename, "seniority": seniority}
