from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from backend.api.v1.controllers.predict_controller import extract_text_from_pdf
from backend.api.v1.controllers.skills_controller import (
    extract_skills,
    match_jobs,
    get_missing_skills_by_job
)

router = APIRouter(tags=["Skills"])

class TextInput(BaseModel):
    text: str

@router.post("/extract_skills_from_pdf")
async def extract_skills_from_pdf(file: UploadFile = File(...)):
    pdf_bytes = await file.read()  # read bytes like predict_pdf
    text = extract_text_from_pdf(pdf_bytes)  # reuse your PDF-to-text function
    skills_detected = extract_skills(text)
    ranking = match_jobs(skills_detected)
    missing = get_missing_skills_by_job(skills_detected)
    return {
        "extracted_skills": skills_detected,
        "ranking": ranking,
        "missing_skills_by_job": missing
    }
