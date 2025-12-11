from fastapi import FastAPI, APIRouter, UploadFile, File
from pydantic import BaseModel
import io
import pdfplumber
from skills_logic import match_jobs

app = FastAPI(
    title="Skills-to-Jobs Ranking API",
    description="Ranking de roles según las skills del usuario",
    version="1.0",
)

router = APIRouter()

class SkillInput(BaseModel):
    skills: list[str]

# ---------------------------
# Endpoint para skills directas
# ---------------------------
@router.post("/rank_jobs_by_skills")
def rank_jobs_by_skills(data: SkillInput):
    ranking = match_jobs(data.skills)
    return {
        "skills_provided": data.skills,
        "ranking": [
            {"job_title": job, "matching_skills": count}
            for job, count in ranking
        ]
    }

# ---------------------------
# Endpoint para PDF
# ---------------------------
@router.post("/rank_jobs_from_pdf")
async def rank_jobs_from_pdf(file: UploadFile = File(...)):
    """
    Sube un PDF y obtiene un ranking de roles según las skills encontradas en el texto.
    """

    # 1. Leer PDF en bytes
    pdf_bytes = await file.read()

    # 2. Convertir bytes → archivo en memoria
    pdf_file = io.BytesIO(pdf_bytes)

    # 3. Extraer texto
    try:
        with pdfplumber.open(pdf_file) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    except Exception as e:
        return {"error": f"No se pudo leer el PDF: {str(e)}"}

    if not text.strip():
        return {"error": "El PDF no contiene texto legible."}

    # 4. Procesar texto y obtener ranking
    words = [w.lower().strip() for w in text.replace(",", "\n").split()]
    ranking = match_jobs(words)

    return {
        "filename": file.filename,
        "ranking": [
            {"job_title": job, "matching_skills": count}
            for job, count in ranking
        ]
    }

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    print("Running FastAPI app on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
