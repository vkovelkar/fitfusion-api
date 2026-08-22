import pytest

from tools.fitness.analyze import analyze_fitness


# ============================================================
# BASE VALID INPUT
# ============================================================

@pytest.fixture
def valid_data():
    """
    Returns a fresh valid fitness profile
    for every test.
    """

    return {
        "name": "Vijay",
        "age": 35,
        "gender": "male",
        "weight": 72.5,
        "height": 175,
        "activity_level": "moderate",
        "goal": "fat_loss"
    }


# ============================================================
# SUCCESS TEST
# ============================================================

def test_analyze_fitness_success(valid_data):

    result = analyze_fitness(valid_data)

    # Response should not contain an error.
    assert "error" not in result

    # Main sections should exist.
    assert "profile" in result
    assert "analysis" in result

    # Check profile values.
    assert result["profile"]["age"] == 35
    assert result["profile"]["gender"] == "male"
    assert result["profile"]["weight_kg"] == 72.5
    assert result["profile"]["height_cm"] == 175
    assert result["profile"]["goal"] == "fat_loss"

    # Check calculated values.
    assert result["analysis"]["bmi"] > 0
    assert result["analysis"]["bmr_calories"] > 0
    assert result["analysis"]["maintenance_calories"] > 0
    assert result["analysis"]["target_calories"] > 0

    # Check macros.
    assert "macros" in result["analysis"]

    assert result["analysis"]["macros"]["protein_g"] > 0
    assert result["analysis"]["macros"]["fat_g"] > 0
    assert result["analysis"]["macros"]["carbohydrates_g"] > 0


# ============================================================
# FEMALE PROFILE TEST
# ============================================================

def test_analyze_fitness_female(valid_data):

    data = valid_data.copy()

    data["gender"] = "female"

    result = analyze_fitness(data)

    assert "error" not in result

    assert result["profile"]["gender"] == "female"

    assert result["analysis"]["bmr_calories"] > 0


# ============================================================
# TEST ALL FITNESS GOALS
# ============================================================

@pytest.mark.parametrize(
    "goal",
    [
        "fat_loss",
        "maintenance",
        "muscle_gain"
    ]
)
def test_valid_goals(valid_data, goal):

    data = valid_data.copy()

    data["goal"] = goal

    result = analyze_fitness(data)

    assert "error" not in result

    assert result["profile"]["goal"] == goal


# ============================================================
# MISSING REQUIRED FIELDS
# ============================================================

@pytest.mark.parametrize(
    "field",
    [
        "name",
        "age",
        "gender",
        "weight",
        "height",
        "activity_level",
        "goal"
    ]
)
def test_missing_required_fields(valid_data, field):

    data = valid_data.copy()

    del data[field]

    result = analyze_fitness(data)

    assert "error" in result


# ============================================================
# INVALID INPUT TESTS
# ============================================================

@pytest.mark.parametrize(
    "field,value,expected_error",
    [

        (
            "name",
            "",
            "name cannot be empty"
        ),

        (
            "age",
            "thirty five",
            "age must be a number"
        ),

        (
            "age",
            -35,
            "age must be between 1 and 120"
        ),

        (
            "gender",
            "robot",
            "Invalid gender"
        ),

        (
            "weight",
            "seventy",
            "weight must be a number"
        ),

        (
            "weight",
            -72.5,
            "weight must be between 1 and 500"
        ),

        (
            "height",
            "one seventy five",
            "height must be a number"
        ),

        (
            "height",
            -175,
            "height must be between 1 and 300"
        ),

        (
            "activity_level",
            "super_active",
            "Invalid activity_level"
        ),

        (
            "goal",
            "become_superhuman",
            "Invalid goal"
        )
    ]
)
def test_invalid_inputs(
    valid_data,
    field,
    value,
    expected_error
):

    data = valid_data.copy()

    data[field] = value

    result = analyze_fitness(data)

    assert "error" in result

    assert result["error"] == expected_error