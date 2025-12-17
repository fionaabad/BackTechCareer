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

from backend.api.v1.controllers.salary_controller import (
    predict_salary_from_profile,
)

router = APIRouter(tags=["Prediction"])


@router.post("/predict_pdf")
async def predict_pdf(
    file: UploadFile = File(...),
    country: str = "ES",
    company_size: str = "M",
    employment_type: str = "FT",
    work_year: int = 2025,
    remote_ratio: int = 50,
):
    # Validació bàsica dels params
    if int(remote_ratio) not in (0, 50, 100):
        raise HTTPException(
            status_code=400,
            detail="remote_ratio ha de ser 0, 50 o 100"
        )

    pdf_bytes = await file.read()
    text = extract_text_from_pdf(pdf_bytes)

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="El PDF no contiene texto legible."
        )

    # Model 1: Role
    try:
        result = predict_text(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error prediciendo rol: {str(e)}")

    # Model 2: Seniority
    try:
        seniority = predict_seniority_from_text(text)
    except Exception:
        seniority = "Unknown"

    # Skills
    extracted_skills = extract_skills(text)

    top3 = result.get("top3", [])
    predicted_job_titles = [item.get("job_title") for item in top3 if item.get("job_title")]

    skills_details = skills_for_jobs(
        skills=extracted_skills,
        predicted_jobs=predicted_job_titles,
    )

    # Model 3: Salary (només si seniority és usable)
    salary = None
    if seniority != "Unknown":
        try:
            salary = predict_salary_from_profile(
                role_label=result.get("prediccion", ""),
                seniority=seniority,
                country=country,
                company_size=company_size,
                employment_type=employment_type,
                work_year=work_year,
                remote_ratio=remote_ratio,
            )
        except Exception:
            salary = None

    return {
        "filename": file.filename,
        "texto_extraido": text[:15000],
        "prediccion": result.get("prediccion"),
        "top3": top3,
        "probabilidades": result.get("probabilidades", {}),
        "seniority": seniority,
        "skills": extracted_skills,
        "skills_details": skills_details,
        "salary": salary,
        "salary_params_used": {
            "country": country,
            "company_size": company_size,
            "employment_type": employment_type,
            "work_year": work_year,
            "remote_ratio": remote_ratio,
        },
    }
