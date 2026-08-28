import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "workout_data.csv"
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "calorie_prediction_pipeline.joblib"
)


FEATURE_COLUMNS = [
    "age",
    "weight",
    "height",
    "duration",
    "heart_rate",
    "workout_type"
]


def evaluate_model():

    print("Loading raw data...")

    df = pd.read_csv(DATA_PATH)

    X = df[FEATURE_COLUMNS]

    y = df["calories_burned"]

    _, X_test, _, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    print("Loading ML pipeline...")

    pipeline = joblib.load(MODEL_PATH)

    print("Running predictions...")

    predictions = pipeline.predict(X_test)

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    mse = mean_squared_error(
        y_test,
        predictions
    )

    rmse = mse ** 0.5

    r2 = r2_score(
        y_test,
        predictions
    )

    print("\n" + "=" * 50)
    print("ML PIPELINE EVALUATION RESULTS")
    print("=" * 50)

    print(f"MAE  : {mae:.2f}")
    print(f"MSE  : {mse:.2f}")
    print(f"RMSE : {rmse:.2f}")
    print(f"R²   : {r2:.4f}")

    return {
        "mae": float(mae),
        "mse": float(mse),
        "rmse": float(rmse),
        "r2": float(r2)
    }


if __name__ == "__main__":

    evaluate_model()