import json
from json import JSONDecodeError
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

DATA_DIR = Path(__file__).resolve().parent
CLEAN_FILE = DATA_DIR / "activity_cleaned.json"
RAW_FILE = DATA_DIR / "activity.json"
MODEL_FILE = DATA_DIR / "activity_type_model.joblib"


def load_dataset() -> pd.DataFrame:
    source_file = CLEAN_FILE if CLEAN_FILE.exists() else RAW_FILE

    with source_file.open("r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except JSONDecodeError as exc:
            raise ValueError(
                f"JSON yüklenirken hata oluştu: {exc}. "
                "Önce data_processing/fix_activity_json.py scriptini çalıştırın."
            ) from exc

    if not isinstance(data, list):
        raise ValueError("Veri dosyası bir liste içermelidir.")

    df = pd.DataFrame(data)

    if "price" in df.columns:
        df = df.drop(columns=["price"])

    df = df[ [col for col in ["activity", "type", "participants"] if col in df.columns] ]
    df = df.dropna(subset=["activity", "type", "participants"])
    df["activity"] = df["activity"].astype(str)
    df["type"] = df["type"].astype(str)
    df["participants"] = df["participants"].astype(int)

    return df


def build_pipeline() -> Pipeline:
    text_transformer = Pipeline(
        steps=[
            ("tfidf", TfidfVectorizer(max_features=5000, ngram_range=(1, 2)))
        ]
    )

    numeric_transformer = "passthrough"

    preprocessor = ColumnTransformer(
        transformers=[
            ("text", text_transformer, "activity"),
            ("participants", numeric_transformer, ["participants"]),
        ],
        remainder="drop",
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", RandomForestClassifier(n_estimators=200, random_state=42)),
        ]
    )

    return pipeline


def train_and_save_model(df: pd.DataFrame) -> None:
    X = df[["activity", "participants"]]
    y = df["type"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Classification report:\n", classification_report(y_test, y_pred, zero_division=0))

    joblib.dump(pipeline, MODEL_FILE)
    print(f"Model kaydedildi: {MODEL_FILE}")


def main() -> None:
    df = load_dataset()
    train_and_save_model(df)


if __name__ == "__main__":
    main()
