from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
import pdfplumber
import io
from pathlib import Path   # <--- añadido para rutas

# ============================================
#          CARGA DEL MODELO MODERNO
# ============================================

MODEL_PATH = r"C:\Users\dlope\Desktop\ProyectoFinal\modelo2\modelo_moderno.pkl"
VECTORIZER_PATH = r"C:\Users\dlope\Desktop\ProyectoFinal\modelo2\tfidf_vectorizer_moderno.pkl"
ENCODER_PATH = r"C:\Users\dlope\Desktop\ProyectoFinal\modelo2\label_encoder_moderno.pkl"

modelo = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)
label_encoder = joblib.load(ENCODER_PATH)

# ============================================
#       CARGA DEL MODELO DE SENIORITY
# ============================================

SENIORITY_MODEL_PATH = r"C:\Users\dlope\Desktop\ProyectoFinal\backGit\TechCareer\backend\ml\models\seniority\seniority_from_cv_balanced_v1.pkl"

model_seniority = joblib.load(SENIORITY_MODEL_PATH)

# ============================================
#          INICIAR FASTAPI
# ============================================

app = FastAPI(
    title="Modern Job Prediction API",
    description="Clasificación moderna + seniority",
    version="2.1",
)

# ============================================
#                    CORS
# ============================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          
    allow_credentials=True,
    allow_methods=["*"],          
    allow_headers=["*"],          
)

# ============================================
#       MODELO DE ENTRADA PARA TEXTO
# ============================================

class CVInput(BaseModel):
    cv_text: str

# ============================================
#          FUNCIÓN DE PREDICCIÓN MODERNA
# ============================================

def predecir(cv_text: str):
    vector = vectorizer.transform([cv_text]).toarray()
    probs = modelo.predict_proba(vector)[0]

    best_idx = int(np.argmax(probs))
    best_title = label_encoder.inverse_transform([best_idx])[0]

    top3_idx = probs.argsort()[-3:][::-1]
    top3 = [
        {
            "job_title": label_encoder.inverse_transform([i])[0],
            "prob": float(probs[i]),
        }
        for i in top3_idx
    ]

    probs_dict = {
        label_encoder.inverse_transform([i])[0]: float(prob)
        for i, prob in enumerate(probs)
    }

    return {
        "prediccion": best_title,
        "top3": top3,
        "probabilidades": probs_dict,
    }

# ============================================
#     FUNCIÓN PARA PREDICCIÓN DE SENIORITY
# ============================================

def predecir_seniority(cv_text: str):
    return model_seniority.predict([cv_text])[0]

# ============================================
#          ENDPOINT — /predict (Texto)
# ============================================

@app.post("/predict")
def predict_endpoint(data: CVInput):
    return predecir(data.cv_text)

# ============================================
#          ENDPOINT — /predict_pdf (PDF)
# ============================================

@app.post("/predict_pdf")
async def predict_from_pdf(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    pdf_file = io.BytesIO(pdf_bytes)

    try:
        with pdfplumber.open(pdf_file) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    except Exception as e:
        return {"error": f"No se pudo leer el PDF: {str(e)}"}

    if not text.strip():
        return {"error": "El PDF no contiene texto legible."}

    resultado = predecir(text)

    return {
        "filename": file.filename,
        "texto_extraido": text[:15000],
        "prediccion": resultado["prediccion"],
        "top3": resultado["top3"],
        "probabilidades": resultado["probabilidades"],
    }

# ============================================
#     ENDPOINT — /predict_seniority (Solo Seniority)
# ============================================

@app.post("/predict_seniority")
def predict_seniority_endpoint(data: CVInput):
    seniority = predecir_seniority(data.cv_text)
    return {"seniority": seniority}
