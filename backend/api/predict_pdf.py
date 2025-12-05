from fastapi import FastAPI, UploadFile, File
import pdfplumber

# ... (todo lo demás de tu API queda igual)

@app.post("/predict_pdf")
async def predict_from_pdf(file: UploadFile = File(...)):
    """
    Sube un PDF y el endpoint devuelve la predicción del rol.
    """

    # 1. Leer PDF en memoria
    pdf_bytes = await file.read()

    # 2. Extraer texto del PDF
    try:
        with pdfplumber.open(bytes(pdf_bytes)) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    except Exception as e:
        return {"error": f"No se pudo leer el PDF: {str(e)}"}

    if not text.strip():
        return {"error": "El PDF no contiene texto legible."}

    # 3. Llamar a la función de predicción existente
    resultado = predecir(text)

    return {
        "filename": file.filename,
        "texto_extraido": text[:8000],  # opcional: devolver primeros 8000 chars
        "prediccion": resultado["prediccion"],
        "top3": resultado["top3"],
        "probabilidades": resultado["probabilidades"]
    }
