
from pathlib import Path
import json
import joblib
import mlflow
import mlflow.sklearn
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "student_placement.csv"
MODEL_DIR = ROOT / "artifacts"

TARGET = "placed"
FEATURES = [
    "cgpa",
    "coding_score",
    "aptitude_score",
    "projects",
    "internships"
]


def build_pipeline():
    numeric = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    prep = ColumnTransformer([
        ("numeric", numeric, FEATURES)
    ])

    model = Pipeline([
        ("preprocessing", prep),
        ("classifier", LogisticRegression(max_iter=1000))
    ])

    return model


def train(data_path=DATA):
    # Load dataset
    df = pd.read_csv(data_path)

    # Validate required columns
    required_columns = FEATURES + [TARGET]
    missing_columns = [
        col for col in required_columns if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

    if df.empty:
        raise ValueError("Dataset is empty")

    X = df[FEATURES]
    y = df[TARGET]

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # Train model
    model = build_pipeline()
    model.fit(X_train, y_train)

    # Predictions
    pred = model.predict(X_test)
    prob = model.predict_proba(X_test)[:, 1]

    # Calculate metrics
    metrics = {
        "accuracy": float(accuracy_score(y_test, pred)),
        "precision": float(
            precision_score(y_test, pred, zero_division=0)
        ),
        "recall": float(
            recall_score(y_test, pred, zero_division=0)
        ),
        "f1": float(f1_score(y_test, pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_test, prob))
    }

    # Create output directory
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    # Configure MLflow
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("student-placement")

    # Log experiment
    with mlflow.start_run() as run:
        mlflow.log_param("model", "LogisticRegression")
        mlflow.log_param("test_size", 0.2)
        mlflow.log_param("random_state", 42)
        mlflow.log_metrics(metrics)

        # Log model to MLflow
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            skops_trusted_types=["numpy.dtype"]
        )

        # Save model locally
        joblib.dump(
            model,
            MODEL_DIR / "placement_model.joblib"
        )

        # Save metrics locally
        (MODEL_DIR / "metrics.json").write_text(
            json.dumps(metrics, indent=2),
            encoding="utf-8"
        )

        print("Run ID:", run.info.run_id)
        print("Metrics:")
        print(json.dumps(metrics, indent=2))

    return metrics


if __name__ == "__main__":
    train()
