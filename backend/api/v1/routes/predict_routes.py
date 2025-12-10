from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from backend.api.v1.controllers.predict_controller import (
    extract_text_from_pdf, 
    predict_text
)
from backend.api.v1.controllers.skills_controller import (
    extract_skills_from_text,
    rank_jobs_from_skills,
    get_skills_from_resume,
    get_missing_skills
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

# skills

class SkillInput(BaseModel):
    skills: list[str]

@router.post("/predict_skills")
async def predict_skills(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    text = extract_text_from_pdf(pdf_bytes)
    if not text.strip():
        return {"error": "El PDF no contiene texto legible."}

    skills = extract_skills_from_text(text)
    ranking = rank_jobs_from_skills(skills)
    missing = get_missing_skills(skills)

    return {
        "filename": file.filename,
        "extracted_skills": skills,
        "ranking": ranking,
        "missing_skills_by_job": missing
    }

@router.post("/rank_jobs_by_skills")
def rank_jobs_by_skills(data: SkillInput):
    ranking = rank_jobs_from_skills(data.skills)
    missing = get_missing_skills(data.skills)
    return {
        "skills_provided": data.skills,
        "ranking": ranking,
        "missing_skills_by_job": missing
    }

@router.post("/rank_jobs_from_pdf")
async def rank_jobs_from_pdf(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    text = extract_text_from_pdf(pdf_bytes)
    if not text.strip():
        return {"error": "El PDF no contiene texto legible."}

    skills = extract_skills_from_text(text)
    ranking = rank_jobs_from_skills(skills)
    missing = get_missing_skills(skills)

