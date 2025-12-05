import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
DATA_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "data",
    "model1_cv_role",
    "3.processed",
    "v1_english",
    "cv_labeled_final.csv"
)

MODEL_DIR = os.path.join(BASE_DIR, "models", "cv_role")


def ensure_dirs():
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)


def load_data():
    df = pd.read_csv(DATA_PATH)
    X = df["cv_text"]
    y = df["role_label_final"]
    return X, y


def train_model(X, y):
    vectorizer = TfidfVectorizer(
        max_features=20000,
        ngram_range=(1, 2),
        stop_words="english"
    )
    X_vec = vectorizer.fit_transform(X)
    model = LogisticRegression(max_iter=4000)
    model.fit(X_vec, y)
    return model, vectorizer


def evaluate(model, vectorizer, X, y):
    X_vec = vectorizer.transform(X)
    preds = model.predict(X_vec)
    print("\n=== Evaluation Report ===\n")
    print(classification_report(y, preds))


def compute_top3_accuracy(model, vectorizer, X, y):
    proba = model.predict_proba(vectorizer.transform(X))
    classes = model.classes_
    correct = 0

    for p, y_true in zip(proba, y):
        top3 = p.argsort()[-3:]
        if y_true in classes[top3]:
            correct += 1

    score = correct / len(y)
    print("Top-3 Accuracy:", score)


def save_artifacts(model, vectorizer):
    joblib.dump(model, os.path.join(MODEL_DIR, "model.pkl"))
    joblib.dump(vectorizer, os.path.join(MODEL_DIR, "vectorizer.pkl"))
    print("Model and vectorizer saved.")


def main():
    ensure_dirs()

    print("Loading dataset...")
    X, y = load_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    print("Training model...")
    model, vectorizer = train_model(X_train, y_train)

    print("Evaluating model...")
    evaluate(model, vectorizer, X_test, y_test)
    compute_top3_accuracy(model, vectorizer, X_test, y_test)

    print("Saving artifacts...")
    save_artifacts(model, vectorizer)

    print("Training completed.")
    # asdas


if __name__ == "__main__":
    main()
