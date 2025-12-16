# api/v1/controllers/seniority_controller.py

import os
import joblib

# Ruta relativa (igual que el resto del proyecto)
SENIORITY_MODEL_PATH = "backend/ml/models/seniority/seniority_from_cv_balanced_v1.pkl"

# Cache en memoria (para no recargar el .pkl en cada request)
_model_seniority = None


def get_seniority_model():
    """
    Carga el modelo de seniority una sola vez y lo deja en caché.
    Lanza FileNotFoundError si el archivo no existe.
    """
    global _model_seniority

    if _model_seniority is not None:
        return _model_seniority

    if not os.path.exists(SENIORITY_MODEL_PATH):
        raise FileNotFoundError(
            f"Seniority model not found at: {SENIORITY_MODEL_PATH}"
        )

    _model_seniority = joblib.load(SENIORITY_MODEL_PATH)
    return _model_seniority


def predict_seniority_from_text(cv_text: str) -> str:
    """
    Predice seniority a partir del texto del CV.
    Devuelve la etiqueta (string) que predice el modelo.
    """
    text = (cv_text or "").strip()
    if not text:
        raise ValueError("Empty CV text")

    model = get_seniority_model()

    # Mismo patrón que en tu api3.py: predict sobre lista de strings
    pred = model.predict([text])[0]

    # Normalizamos a string por si el modelo devuelve numpy types
    return str(pred)
