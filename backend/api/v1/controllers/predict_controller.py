import io
import joblib
import numpy as np
import pdfplumber

MODEL_PATH = "backend/ml/models/cv_role/model.pkl"
VECTORIZER_PATH = "backend/ml/models/cv_role/vectorizer.pkl"

modelo = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    pdf_file = io.BytesIO(pdf_bytes)
    with pdfplumber.open(pdf_file) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)

def predict_text(cv_text: str):
    vector = vectorizer.transform([cv_text]).toarray()
    probs = modelo.predict_proba(vector)[0]

    best_idx = int(np.argmax(probs))
    best_title = modelo.classes_[best_idx]

    top3_idx = probs.argsort()[-3:][::-1]
    top3 = [
        {
            "job_title": modelo.classes_[i],
            "prob": float(probs[i]),
        }
        for i in top3_idx
    ]

    probs_dict = {
        modelo.classes_[i]: float(prob)
        for i, prob in enumerate(probs)
    }

    return {
        "prediccion": best_title,
        "top3": top3,
        "probabilidades": probs_dict
    }
