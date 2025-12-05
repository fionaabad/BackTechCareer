from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
import pdfplumber
import io

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
#          INICIAR FASTAPI
# ============================================

app = FastAPI(
    title="Modern Job Prediction API",
    description="Clasificación moderna de CVs con 16 roles técnicos reales",
    version="2.0",
)

# ============================================
#                    CORS
# ============================================
# NECESARIO PARA QUE TU WEB FUNCIONE DESDE ARCHIVO LOCAL (origin null)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Permite a cualquier web conectarse
    allow_credentials=True,
    allow_methods=["*"],          # GET, POST, etc.
    allow_headers=["*"],          # Headers permitidos
)

# ============================================
#       MODELO DE ENTRADA /predict (JSON)
# ============================================

class CVInput(BaseModel):
    cv_text: str

# ============================================
#          FUNCIÓN DE PREDICCIÓN GENERAL
# ============================================

def predecir(cv_text: str):
    vector = vectorizer.transform([cv_text]).toarray()
    probs = modelo.predict_proba(vector)[0]

    # índice de categoría con mayor probabilidad
    best_idx = int(np.argmax(probs))
    best_title = label_encoder.inverse_transform([best_idx])[0]

    # TOP-3
    top3_idx = probs.argsort()[-3:][::-1]
    top3 = [
        {
            "job_title": label_encoder.inverse_transform([i])[0],
            "prob": float(probs[i]),
        }
        for i in top3_idx
    ]

    # Todas las probabilidades
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
#          ENDPOINT 1 — /predict (Texto)
# ============================================

@app.post("/predict")
def predict_endpoint(data: CVInput):
    return predecir(data.cv_text)

# ============================================
#          ENDPOINT 2 — /predict_pdf (PDF)
# ============================================

@app.post("/predict_pdf")
async def predict_from_pdf(file: UploadFile = File(...)):
    """
    Sube un PDF y obtiene una predicción del rol profesional usando el modelo moderno.
    """

    # 1. Leer PDF en bytes
    pdf_bytes = await file.read()

    # 2. Convertir bytes → archivo en memoria (NECESARIO para pdfplumber)
    pdf_file = io.BytesIO(pdf_bytes)

    # 3. Extraer texto del PDF
    try:
        with pdfplumber.open(pdf_file) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    except Exception as e:
        return {"error": f"No se pudo leer el PDF: {str(e)}"}

    if not text.strip():
        return {"error": "El PDF no contiene texto legible."}

    # 4. Predicción usando el modelo
    resultado = predecir(text)

    # 5. Respuesta completa
    return {
        "filename": file.filename,
        "texto_extraido": text[:15000],   # hasta 15k caracteres
        "prediccion": resultado["prediccion"],
        "top3": resultado["top3"],
        "probabilidades": resultado["probabilidades"],
    }
