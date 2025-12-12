import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib


def train_seniority_model(
    csv_path: str = r"C:\Users\dlope\Desktop\ProyectoFinal\backGit\TechCareer\backend\ml\data\model2_seniority\3.processed\cv_with_seniority_weak.csv",
    model_output: str = r"C:\Users\dlope\Desktop\ProyectoFinal\backGit\TechCareer\backend\ml\models\seniority\seniority_from_cv_balanced_v1.pkl"
):
    """
    Entrena un modelo de clasificación de seniority (Junior, Mid, Senior)
    a partir del texto de CVs y guarda el modelo resultante en un archivo .pkl.
    """

    print("📌 Cargando dataset desde:", csv_path)
    df = pd.read_csv(csv_path, encoding="utf-8")

    # Filtrar etiquetas válidas
    VALID_LABELS = ["Junior", "Mid", "Senior"]
    df = df[df["seniority_weak"].isin(VALID_LABELS)]

    print(f"📊 Total muestras válidas: {len(df)}")

    # Dividir datos
    df_train, df_test = train_test_split(
        df,
        test_size=0.2,
        random_state=42,
        stratify=df["seniority_weak"]
    )

    print("🔧 Entrenando modelo...")

    pipeline = Pipeline(
        steps=[
            ("tfidf", TfidfVectorizer(
                lowercase=True,
                stop_words="english",
                ngram_range=(1, 2),
                min_df=5,
                max_df=0.8
            )),
            ("clf", LogisticRegression(
                max_iter=1000,
                n_jobs=-1
            )),
        ]
    )

    pipeline.fit(df_train["cv_text"], df_train["seniority_weak"])

    # Evaluación
    print("\n📈 Resultados en Test:")
    y_pred = pipeline.predict(df_test["cv_text"])
    print(classification_report(df_test["seniority_weak"], y_pred))

    # Guardar modelo
    model_output = Path(model_output)
    model_output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, model_output)

    print("\n✅ Modelo guardado en:", model_output)


if __name__ == "__main__":
    train_seniority_model()
