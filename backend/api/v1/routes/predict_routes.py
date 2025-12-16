from fastapi import APIRouter, UploadFile, File, HTTPException

from backend.api.v1.controllers.predict_controller import (
    extract_text_from_pdf,
    predict_text,
    extract_skills,
    skills_for_jobs,
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
        raise HTTPException(
            status_code=400,
            detail="El PDF no contiene texto legible."
        )

    result = predict_text(text)

    try:
        seniority = predict_seniority_from_text(text)
    except Exception:
        seniority = "Unknown"

    extracted_skills = extract_skills(text)

    predicted_job_titles = [
        item["job_title"] for item in result["top3"]
    ]

    skills_details = skills_for_jobs(
        skills=extracted_skills,
        predicted_jobs=predicted_job_titles,
    )

    return {
        "filename": file.filename,
        "texto_extraido": text[:15000],
        "prediccion": result["prediccion"],
        "top3": result["top3"],
        "probabilidades": result["probabilidades"],
        "seniority": seniority,
        "skills": extracted_skills,
        "skills_details": skills_details,
    }
