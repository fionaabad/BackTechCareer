from fastapi import APIRouter
from pydantic import BaseModel
from backend.api.v1.controllers.analyze_controller import analyze_cv

router = APIRouter()

class CVRequest(BaseModel):
    cv_text: str

@router.post("/analyze-cv")
def analyze(request: CVRequest):
    return analyze_cv(request.cv_text)
