import os
import pytest

from ml.src.train import train_model
from ml.src.predict import predict_calories


# =========================================================
# TEST: MODEL FILE IS CREATED
# =========================================================

def test_model_file_exists():

    train_model()

    model_path = "ml/models/calorie_prediction_pipeline.joblib"

    assert os.path.exists(model_path)


# =========================================================
# TEST: VALID CALORIE PREDICTION
# =========================================================

def test_model_prediction():

    train_model()

    prediction = predict_calories(
        age=35,
        weight=72.5,
        height=175,
        duration=45,
        heart_rate=135,
        workout_type="Running"
    )

    assert prediction is not None

    assert isinstance(prediction, float)

    assert prediction > 0


# =========================================================
# TEST: INVALID WORKOUT TYPE
# =========================================================

def test_invalid_workout_type():

    train_model()

    with pytest.raises(ValueError):

        predict_calories(
            age=35,
            weight=72.5,
            height=175,
            duration=45,
            heart_rate=135,
            workout_type="Swimming"
        )


# =========================================================
# TEST: INVALID NUMERIC INPUT
# =========================================================

def test_invalid_duration():

    train_model()

    with pytest.raises(ValueError):

        predict_calories(
            age=35,
            weight=72.5,
            height=175,
            duration=-10,
            heart_rate=135,
            workout_type="Running"
        )