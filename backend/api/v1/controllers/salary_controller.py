# backend/api/v1/controllers/salary_controller.py
from __future__ import annotations

import os
from typing import Any, Dict, Tuple

import joblib
import numpy as np
import pandas as pd

SALARY_MODEL_PATH = "backend/ml/models/salaries/v3_salary_from_profile_hgb.pkl"

# Cache en memòria
_salary_model = None

# --- FX (simple, deterministic) ---
# ECB euro reference rate: 1 EUR = 1.1776 USD (16 Dec 2025)
# So: EUR = USD / 1.1776
USD_PER_EUR = 1.1776
FX_DATE = "2025-12-16"
FX_SOURCE = "ECB euro reference rate"

# Mapping: Model 1 role -> role_label_salary (model 3)
ROLE_TO_SALARY_ROLE: Dict[str, str] = {
    # Data / ML
    "data_scientist": "data_scientist",
    "data_engineer": "data_engineer",
    "data_analyst": "data_analyst",
    "machine_learning_engineer": "machine_learning_engineer",
    "ml_engineer": "machine_learning_engineer",
    "bi_engineer": "bi_engineer",
    "data_architect": "data_architect",
    "data_manager": "data_manager",
    "data_director": "data_director",
    "research_scientist": "research_scientist",

    # Software roles -> fora d'scope
    "python_developer": "other",
    "backend_developer": "other",
    "frontend_developer": "other",
    "fullstack_developer": "other",
}

DEFAULTS = {
    "country": "ES",
    "company_size": "M",
    "employment_type": "FT",
    "work_year": 2025,
    "remote_ratio": 50,
}


def get_salary_model() -> Any:
    global _salary_model
    if _salary_model is not None:
        return _salary_model

    if not os.path.exists(SALARY_MODEL_PATH):
        raise FileNotFoundError(f"Salary model not found at: {SALARY_MODEL_PATH}")

    _salary_model = joblib.load(SALARY_MODEL_PATH)
    return _salary_model


def normalize_seniority(s: str) -> str:
    """
    Normalitza a la forma esperada pel model (ex: 'junior','mid','senior','lead').
    Funciona amb 'Junior', 'MID', etc.
    """
    s = (s or "").strip().lower()
    mapping = {
        "jr": "junior",
        "junior": "junior",
        "entry": "junior",
        "mid": "mid",
        "middle": "mid",
        "intermediate": "mid",
        "sr": "senior",
        "senior": "senior",
        "lead": "lead",
        "principal": "lead",
        "staff": "lead",
    }
    return mapping.get(s, s)


def map_role_to_salary_role(role_label: str) -> Tuple[str, str]:
    """
    Retorna (role_label_salary, notes)
    """
    rl = (role_label or "").strip().lower()
    if not rl:
        return "other", "role_label buit -> mapejat a 'other'"

    mapped = ROLE_TO_SALARY_ROLE.get(rl, "other")
    if mapped == "other" and rl not in ROLE_TO_SALARY_ROLE:
        return "other", f"role_label '{rl}' fora d'scope -> mapejat a 'other'"

    return mapped, "ok"


def compute_confidence(role_label_salary: str) -> str:
    """
    Heurística simple.
    """
    high = {
        "data_scientist",
        "data_engineer",
        "data_analyst",
        "machine_learning_engineer",
        "bi_engineer",
    }
    medium = {"research_scientist"}
    if role_label_salary in high:
        return "high"
    if role_label_salary in medium:
        return "medium"
    return "low"


def predict_salary_from_profile(
    *,
    role_label: str,
    seniority: str,
    country: str = DEFAULTS["country"],
    company_size: str = DEFAULTS["company_size"],
    employment_type: str = DEFAULTS["employment_type"],
    work_year: int = DEFAULTS["work_year"],
    remote_ratio: int = DEFAULTS["remote_ratio"],
) -> Dict[str, Any]:
    """
    Construeix el DataFrame (1 fila) i prediu salary en USD.
    Assumim que el model retorna log1p(salary) i fem expm1.
    També retornem una conversió a EUR (ECB reference rate).
    """
    if not (seniority or "").strip():
        raise ValueError("seniority és obligatori")

    if int(remote_ratio) not in (0, 50, 100):
        raise ValueError("remote_ratio ha de ser 0, 50 o 100")

    role_label_salary, notes = map_role_to_salary_role(role_label)
    seniority_norm = normalize_seniority(seniority)
    confidence = compute_confidence(role_label_salary)

    model = get_salary_model()

    X = pd.DataFrame([{
        "role_label_salary": role_label_salary,
        "seniority": seniority_norm,
        "country": country,
        "company_size": company_size,
        "employment_type": employment_type,
        "work_year": int(work_year),
        "remote_ratio": int(remote_ratio),
    }])

    pred_log = model.predict(X)[0]
    salary_pred_usd = float(np.expm1(pred_log))

    # Convertim a EUR (simple i transparent)
    salary_pred_eur = float(salary_pred_usd / USD_PER_EUR)

    return {
        # Raw model output
        "salary_pred_usd": salary_pred_usd,
        "currency_model": "USD",

        # Converted output (UI-friendly)
        "salary_pred_eur": salary_pred_eur,
        "currency_display": "EUR",

        # FX metadata (important per no “mentir”)
        "fx_usd_per_eur": USD_PER_EUR,
        "fx_date": FX_DATE,
        "fx_source": FX_SOURCE,

        # Debug/trace
        "role_used": role_label_salary,
        "seniority_used": seniority_norm,
        "confidence": confidence,
        "notes": notes,
        "input_profile": X.to_dict(orient="records")[0],
    }
