# backend/api/v1/controllers/analyze_controller.py

from backend.api.v1.controllers.predict_controller import predict_text
from backend.api.v1.controllers.seniority_controller import predict_seniority_from_text

def analyze_cv(cv_text: str):
    """
    Orquesta el análisis completo del CV usando los modelos existentes.
    """

    # 1️⃣ Rol / perfil
    role_result = predict_text(cv_text)
    role = role_result.get("prediccion")

    # 2️⃣ Seniority
    seniority = predict_seniority_from_text(cv_text)

    # 3️⃣ Salary (pendiente)
    salary = None  # placeholder hasta que exista el modelo

    return {
        "role": role,
        "role_details": role_result,   # top3 + probabilidades (muy PRO)
        "seniority": seniority,
        "salary": salary
    }
