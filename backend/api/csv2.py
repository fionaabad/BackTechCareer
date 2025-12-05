import pandas as pd
import json

# === RUTAS ===
INPUT_CSV = r"C:\Users\dlope\Desktop\ProyectoFinal\modelo2\cv_labeled_final.csv"
OUTPUT_JSONL = r"C:\Users\dlope\Desktop\ProyectoFinal\modelo2\cv_dataset_moderno.jsonl"

# === CAMPOS DEL CSV (ajusta si tu CSV tiene otros nombres) ===
TEXT_FIELD = "cv_text"              # Texto del CV
LABEL_FIELD = "role_label_final"    # Etiqueta limpia
ID_FIELD = "cv_id"                  # ID del CV

# ============================================

print("📂 Leyendo CSV desde:", INPUT_CSV)
df = pd.read_csv(INPUT_CSV)

print("✔️ Registros cargados:", len(df))

with open(OUTPUT_JSONL, "w", encoding="utf-8") as f:
    for idx, row in df.iterrows():

        # Si no existe un ID, lo generamos
        cv_id = row[ID_FIELD] if ID_FIELD in df.columns else f"cv_{idx:05d}"

        record = {
            "id": str(cv_id),
            "cv_text": str(row[TEXT_FIELD]),
            "job_title": str(row[LABEL_FIELD]).strip()
        }

        f.write(json.dumps(record, ensure_ascii=False) + "\n")

print("\n🎉 Archivo JSONL creado correctamente:")
print(OUTPUT_JSONL)
