import os
import pandas as pd
import joblib

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split


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


def train_model():

    print("Loading raw data...")

    df = pd.read_csv(DATA_PATH)

    print(f"Dataset shape: {df.shape}")

    # Features
    X = df[
        [
            "age",
            "weight",
            "height",
            "duration",
            "heart_rate",
            "workout_type"
        ]
    ]

    # Target
    y = df["calories_burned"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    categorical_features = [
        "workout_type"
    ]

    numeric_features = [
        "age",
        "weight",
        "height",
        "duration",
        "heart_rate"
    ]

    # Preprocessing
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(
                    handle_unknown="ignore"
                ),
                categorical_features
            ),
            (
                "numeric",
                "passthrough",
                numeric_features
            )
        ]
    )

    # ML model
    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    # Complete ML pipeline
    pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor
            ),
            (
                "model",
                model
            )
        ]
    )

    print("Training ML pipeline...")

    pipeline.fit(
        X_train,
        y_train
    )

    os.makedirs(
        os.path.dirname(MODEL_PATH),
        exist_ok=True
    )

    joblib.dump(
        pipeline,
        MODEL_PATH
    )

    print(
        f"Pipeline saved to: {MODEL_PATH}"
    )

    return pipeline


if __name__ == "__main__":

    train_model()

    print(
        "\nML pipeline training completed successfully."
    )