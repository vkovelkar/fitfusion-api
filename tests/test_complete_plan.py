import pytest

from tools.fitness.plan import (
    generate_complete_plan
)


# ============================================================
# BASE VALID INPUT
# ============================================================

@pytest.fixture
def valid_data():
    """
    Returns a fresh valid fitness profile for every test.
    """

    return {
        "name": "Vijay",
        "age": 35,
        "gender": "male",
        "weight": 72.5,
        "height": 175,
        "activity_level": "moderate",
        "goal": "fat_loss",
        "diet_preference": "vegetarian",
        "experience_level": "intermediate",
        "days_per_week": 5,
        "equipment": "gym"
    }


# ============================================================
# SUCCESS TEST
# ============================================================

def test_generate_complete_plan_success(valid_data):

    result = generate_complete_plan(valid_data)

    # The response should not contain an error.
    assert "error" not in result

    # Check the main sections.
    assert "profile" in result
    assert "analysis" in result
    assert "nutrition_recommendations" in result
    assert "workout_plan" in result

    # Check expected profile values.
    assert result["profile"]["age"] == 35
    assert result["profile"]["goal"] == "fat_loss"

    # Check calculated calories.
    assert result["analysis"]["target_calories"] > 0

    # Check nutrition output.
    assert (
        result["nutrition_recommendations"]
        ["daily_calories"]
        ==
        result["analysis"]["target_calories"]
    )

    # Check workout plan.
    assert (
        len(
            result["workout_plan"]
            ["workout_plan"]
        )
        == 5
    )


# ============================================================
# PARAMETERIZED VALIDATION TESTS
# ============================================================

@pytest.mark.parametrize(
    "field,value,expected_error",
    [

        # Missing name
        (
            "name",
            None,
            "Missing required field: name"
        ),

        # Invalid age type
        (
            "age",
            "thirty five",
            "age must be an integer"
        ),

        # Invalid goal
        (
            "goal",
            "become_superhuman",
            "Invalid goal"
        ),

        # Invalid diet preference
        (
            "diet_preference",
            "vegan",
            "Invalid diet_preference"
        ),

        # Invalid experience level
        (
            "experience_level",
            "expert",
            "Invalid experience_level"
        ),

        # Invalid days per week
        (
            "days_per_week",
            0,
            "days_per_week must be between 1 and 7"
        ),

        # Invalid equipment
        (
            "equipment",
            "spaceship",
            "Invalid equipment"
        ),

        # Invalid weight type
        (
            "weight",
            "seventy",
            "weight must be a number"
        ),

        # Negative weight
        (
            "weight",
            -72.5,
            "weight must be greater than zero"
        )
    ]
)
def test_complete_plan_validation(
    valid_data,
    field,
    value,
    expected_error
):

    # Create a fresh copy.
    data = valid_data.copy()

    # Remove field when value is None.
    if value is None:
        del data[field]

    else:
        data[field] = value

    result = generate_complete_plan(data)

    # The response must contain an error.
    assert "error" in result

    # Verify the expected validation error.
    assert result["error"] == expected_error


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
        "goal",
        "diet_preference",
        "experience_level",
        "days_per_week",
        "equipment"
    ]
)
def test_all_required_fields(valid_data, field):

    data = valid_data.copy()

    # Remove one required field.
    del data[field]

    result = generate_complete_plan(data)

    assert "error" in result

    assert (
        result["error"]
        ==
        f"Missing required field: {field}"
    )