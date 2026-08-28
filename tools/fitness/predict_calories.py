import os

import joblib
import pandas as pd


PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

MODEL_PATH = os.path.join(
    PROJECT_ROOT,
    "ml",
    "models",
    "calorie_prediction_pipeline.joblib"
)


def predict_calories(arguments):

    required_fields = [
        "age",
        "weight",
        "height",
        "duration",
        "heart_rate",
        "workout_type"
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in arguments
    ]

    if missing_fields:
        return {
            "success": False,
            "error": (
                "Missing required fields: "
                + ", ".join(missing_fields)
            )
        }

    if not os.path.exists(MODEL_PATH):
        return {
            "success": False,
            "error": (
                "ML model pipeline not found. "
                "Please train the model first."
            )
        }

    try:

        model = joblib.load(MODEL_PATH)

        input_data = pd.DataFrame([
            {
                "age": arguments["age"],
                "weight": arguments["weight"],
                "height": arguments["height"],
                "duration": arguments["duration"],
                "heart_rate": arguments["heart_rate"],
                "workout_type": arguments["workout_type"]
            }
        ])

        prediction = model.predict(input_data)

        return {
            "success": True,
            "data": {
                "predicted_calories_burned": round(
                    float(prediction[0]),
                    2
                ),
                "model": "calorie_prediction_pipeline"
            }
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error)
        }