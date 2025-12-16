from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

# Reutilitzem el que ja tens (Model 1 + extractor)
from backend.api.v1.controllers.predict_controller import (
    extract_text_from_pdf,
    predict_text,
)

# Reutilitzem el model 2
from backend.api.v1.controllers.seniority_controller import (
    predict_seniority_from_text,
)

# Model 3 (nou)
from backend.api.v1.controllers.salary_controller import (
    predict_salary_from_profile,
)

router = APIRouter(tags=["Salary"])

class SalaryProfileInput(BaseModel):
    role_label: str
    seniority: str
    country: str = "ES"
    company_size: str = "M"
    employment_type: str = "FT"
    work_year: int = 2025
    remote_ratio: int = 50


@router.post("/predict_salary_from_pdf")
async def predict_salary_from_pdf(
    file: UploadFile = File(...),
    country: str = "ES",
    company_size: str = "M",
    employment_type: str = "FT",
    work_year: int = 2025,
    remote_ratio: int = 50,
):
    """
    Orquestra:
    PDF -> text -> role (model1) + seniority (model2) -> salary (model3)
    Amb defaults configurables via query params.
    """
    pdf_bytes = await file.read()
    text = extract_text_from_pdf(pdf_bytes)

    if not text.strip():
        raise HTTPException(status_code=400, detail="El PDF no contiene texto legible.")

    # 1) Role (Model 1)
    try:
        role_result = predict_text(text)
        role_label = role_result["prediccion"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error prediciendo rol: {str(e)}")

    # 2) Seniority (Model 2)
    try:
        seniority = predict_seniority_from_text(text)
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error prediciendo seniority: {str(e)}")

    # 3) Salary (Model 3)
    try:
        salary_result = predict_salary_from_profile(
            role_label=role_label,
            seniority=seniority,
            country=country,
            company_size=company_size,
            employment_type=employment_type,
            work_year=work_year,
            remote_ratio=remote_ratio,
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error prediciendo salary: {str(e)}")

    # Resposta unificada (UI-friendly)
    return {
        "filename": file.filename,
        "role": role_label,
        "seniority": seniority,
        "salary": salary_result,  # inclou salary_pred_usd, confidence, role_used, etc.
        "top3": role_result.get("top3", []),
        "probabilidades": role_result.get("probabilidades", {}),
    }

@router.post("/predict_salary_profile")
def predict_salary_profile(payload: SalaryProfileInput):
    try:
        salary_result = predict_salary_from_profile(
            role_label=payload.role_label,
            seniority=payload.seniority,
            country=payload.country,
            company_size=payload.company_size,
            employment_type=payload.employment_type,
            work_year=payload.work_year,
            remote_ratio=payload.remote_ratio,
        )
        return salary_result

    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error prediciendo salary: {str(e)}")
