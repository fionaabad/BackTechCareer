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

from fastapi import APIRouter
from typing import Dict, List, Any

router = APIRouter(tags=["Salary"])

REMOTE_RATIO_OPTIONS = [
    {"value": 0, "label": "Presencial"},
    {"value": 50, "label": "Híbrido"},
    {"value": 100, "label": "Remoto"},
]

COMPANY_SIZE_OPTIONS = [
    {"value": "S", "label": "Pequeña"},
    {"value": "M", "label": "Mediana"},
    {"value": "L", "label": "Grande"},
]

EMPLOYMENT_TYPE_OPTIONS = [
    {"value": "FT", "label": "Full-time"},
    {"value": "PT", "label": "Part-time"},
    {"value": "CT", "label": "Contrato"},
    {"value": "FL", "label": "Freelance"},
]

WORK_YEAR_OPTIONS = [{"value": y, "label": str(y)} for y in [2020, 2021, 2022, 2023, 2024]]

SENIORITY_OPTIONS = [
    {"value": "junior", "label": "Junior"},
    {"value": "mid", "label": "Mid"},
    {"value": "senior", "label": "Senior"},
    {"value": "lead", "label": "Lead"},
]

# Países: si tienes pycountry, genial; si no, al menos devuelve codes
try:
    import pycountry  # type: ignore

    def country_label(code: str) -> str:
        c = pycountry.countries.get(alpha_2=code)
        return c.name if c else code
except Exception:
    def country_label(code: str) -> str:
        return code

COUNTRY_CODES = [
    # puedes meter los 70, o de momento top + ES, y luego ampliar
    "US","GB","CA","ES","DE","IN","FR","PT","GR","AU","BR","NL","PL","IT","JP","IE","VN",
    "PK","TR","MX","NG","AE","AR","SI","CO","BE","PH","RU","EG","LT"
]

COUNTRY_OPTIONS = [{"value": c, "label": country_label(c)} for c in COUNTRY_CODES]


@router.get("/salary/options")
def salary_options() -> Dict[str, Any]:
    return {
        "country": COUNTRY_OPTIONS,
        "company_size": COMPANY_SIZE_OPTIONS,
        "employment_type": EMPLOYMENT_TYPE_OPTIONS,
        "work_year": WORK_YEAR_OPTIONS,
        "remote_ratio": REMOTE_RATIO_OPTIONS,
        "seniority": SENIORITY_OPTIONS,
    }
