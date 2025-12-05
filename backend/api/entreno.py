import json
import numpy as np
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, top_k_accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# =============================
# RUTAS DE ENTRADA/SALIDA
# =============================
INPUT_JSONL = r"C:\Users\dlope\Desktop\ProyectoFinal\modelo2\cv_dataset_moderno.jsonl"

MODEL_OUT = r"C:\Users\dlope\Desktop\ProyectoFinal\modelo2\modelo_moderno.pkl"
VECTORIZER_OUT = r"C:\Users\dlope\Desktop\ProyectoFinal\modelo2\tfidf_vectorizer_moderno.pkl"
ENCODER_OUT = r"C:\Users\dlope\Desktop\ProyectoFinal\modelo2\label_encoder_moderno.pkl"
REPORT_OUT = r"C:\Users\dlope\Desktop\ProyectoFinal\modelo2\reporte_moderno.txt"

# =============================
# Cargar dataset JSONL
# =============================
print("📂 Cargando JSONL moderno...")
records = []
with open(INPUT_JSONL, "r", encoding="utf-8") as f:
    for line in f:
        records.append(json.loads(line))

print("✔️ Registros cargados:", len(records))

texts = [r["cv_text"] for r in records]
labels = [r["job_title"] for r in records]

# =============================
# Vectorizar texto
# =============================
print("🔠 Entrenando TF-IDF...")
vectorizer = TfidfVectorizer(max_features=5000, stop_words="english")
X = vectorizer.fit_transform(texts).toarray()

joblib.dump(vectorizer, VECTORIZER_OUT)
print("✔️ Guardado vectorizer.")

# =============================
# Codificar etiquetas
# =============================
print("🏷️ Codificando etiquetas...")
encoder = LabelEncoder()
y = encoder.fit_transform(labels)

joblib.dump(encoder, ENCODER_OUT)
print("✔️ Guardado LabelEncoder.")

# =============================
# División train/test
# =============================
print("✂️ Dividiendo train/test...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# =============================
# Entrenar modelo
# =============================
print("🚀 Entrenando modelo moderno...")
clf = LogisticRegression(max_iter=3000)
clf.fit(X_train, y_train)

joblib.dump(clf, MODEL_OUT)
print("✔️ Guardado modelo.")

# =============================
# Evaluación del modelo
# =============================
print("📊 Evaluando...")
pred = clf.predict(X_test)
probs = clf.predict_proba(X_test)

report = classification_report(y_test, pred, target_names=encoder.classes_)
top3 = top_k_accuracy_score(y_test, probs, k=3)

with open(REPORT_OUT, "w", encoding="utf-8") as f:
    f.write(report)
    f.write(f"\nTOP-3 Accuracy: {top3}")

print("\n===== RESULTADOS =====")
print(report)
print("Top-3 Accuracy:", top3)
print("\n🎉 ENTRENAMIENTO COMPLETO.")
