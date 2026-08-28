from pathlib import Path

import joblib
import pandas as pd


# =========================================================
# PATH CONFIGURATION
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "calorie_prediction_pipeline.joblib"
)


# =========================================================
# VALID VALUES
# =========================================================

VALID_WORKOUT_TYPES = [
    "Running",
    "Cycling",
    "Walking",
    "Yoga"
]


# =========================================================
# INPUT VALIDATION
# =========================================================

def validate_input(
    age,
    weight,
    height,
    duration,
    heart_rate,
    workout_type
):

    if age <= 0:
        raise ValueError(
            "Age must be greater than 0"
        )

    if weight <= 0:
        raise ValueError(
            "Weight must be greater than 0"
        )

    if height <= 0:
        raise ValueError(
            "Height must be greater than 0"
        )

    if duration <= 0:
        raise ValueError(
            "Duration must be greater than 0"
        )

    if heart_rate <= 0:
        raise ValueError(
            "Heart rate must be greater than 0"
        )

    if workout_type not in VALID_WORKOUT_TYPES:
        raise ValueError(
            f"Invalid workout type: {workout_type}. "
            f"Valid values are: {', '.join(VALID_WORKOUT_TYPES)}"
        )


# =========================================================
# LOAD MODEL
# =========================================================

def load_model():

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found at: {MODEL_PATH}"
        )

    return joblib.load(MODEL_PATH)


# =========================================================
# PREDICT CALORIES
# =========================================================

def predict_calories(
    age,
    weight,
    height,
    duration,
    heart_rate,
    workout_type
):

    # Validate input before prediction
    validate_input(
        age=age,
        weight=weight,
        height=height,
        duration=duration,
        heart_rate=heart_rate,
        workout_type=workout_type
    )

    model = load_model()

    input_data = pd.DataFrame(
        [
            {
                "age": age,
                "weight": weight,
                "height": height,
                "duration": duration,
                "heart_rate": heart_rate,
                "workout_type": workout_type
            }
        ]
    )

    prediction = model.predict(input_data)

    return float(prediction[0])


# =========================================================
# LOCAL TEST
# =========================================================

if __name__ == "__main__":

    prediction = predict_calories(
        age=35,
        weight=72.5,
        height=175,
        duration=45,
        heart_rate=135,
        workout_type="Running"
    )

    print(
        f"\nPredicted calories burned: "
        f"{prediction:.2f}"
    )