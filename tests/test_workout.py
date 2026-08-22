import pytest

from tools.fitness.workout import workout_plan as generate_workout_plan 


# =========================================================
# VALID INPUT
# =========================================================

@pytest.fixture
def valid_data():

    return {
        "goal": "fat_loss",
        "experience_level": "intermediate",
        "days_per_week": 5,
        "equipment": "gym"
    }


# =========================================================
# SUCCESS TEST
# =========================================================

def test_generate_workout_plan_success(valid_data):

    result = generate_workout_plan(valid_data)

    assert "error" not in result

    assert result["goal"] == "fat_loss"

    assert result["experience_level"] == "intermediate"

    assert result["days_per_week"] == 5

    assert result["equipment"] == "gym"

    assert "workout_plan" in result

    assert isinstance(
        result["workout_plan"],
        list
    )

    assert len(
        result["workout_plan"]
    ) == 5


# =========================================================
# VALID GOALS
# =========================================================

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

    result = generate_workout_plan(data)

    assert "error" not in result

    assert result["goal"] == goal


# =========================================================
# VALID EXPERIENCE LEVELS
# =========================================================

@pytest.mark.parametrize(
    "experience_level",
    [
        "beginner",
        "intermediate",
        "advanced"
    ]
)
def test_valid_experience_levels(
    valid_data,
    experience_level
):

    data = valid_data.copy()

    data["experience_level"] = experience_level

    result = generate_workout_plan(data)

    assert "error" not in result

    assert (
        result["experience_level"]
        == experience_level
    )


# =========================================================
# VALID EQUIPMENT TYPES
# =========================================================

@pytest.mark.parametrize(
    "equipment",
    [
        "gym",
        "home",
        "bodyweight"
    ]
)
def test_valid_equipment(
    valid_data,
    equipment
):

    data = valid_data.copy()

    data["equipment"] = equipment

    result = generate_workout_plan(data)

    assert "error" not in result

    assert result["equipment"] == equipment


# =========================================================
# VALID DAYS PER WEEK
# =========================================================

@pytest.mark.parametrize(
    "days_per_week",
    [
        1,
        2,
        3,
        4,
        5,
        6,
        7
    ]
)
def test_valid_days_per_week(
    valid_data,
    days_per_week
):

    data = valid_data.copy()

    data["days_per_week"] = days_per_week

    result = generate_workout_plan(data)

    assert "error" not in result

    assert (
        result["days_per_week"]
        == days_per_week
    )

    assert len(
        result["workout_plan"]
    ) == days_per_week


# =========================================================
# INVALID GOAL
# =========================================================

def test_invalid_goal(valid_data):

    data = valid_data.copy()

    data["goal"] = "become_superhuman"

    result = generate_workout_plan(data)

    assert "error" in result

    assert result["error"] == "Invalid goal"

    assert "allowed" in result


# =========================================================
# INVALID EXPERIENCE LEVEL
# =========================================================

def test_invalid_experience_level(valid_data):

    data = valid_data.copy()

    data["experience_level"] = "expert"

    result = generate_workout_plan(data)

    assert "error" in result

    assert (
        result["error"]
        == "Invalid experience_level"
    )

    assert "allowed" in result


# =========================================================
# INVALID EQUIPMENT
# =========================================================

def test_invalid_equipment(valid_data):

    data = valid_data.copy()

    data["equipment"] = "spaceship"

    result = generate_workout_plan(data)

    assert "error" in result

    assert result["error"] == "Invalid equipment"

    assert "allowed" in result


# =========================================================
# DAYS PER WEEK TOO LOW
# =========================================================

def test_days_per_week_zero(valid_data):

    data = valid_data.copy()

    data["days_per_week"] = 0

    result = generate_workout_plan(data)

    assert "error" in result

    assert (
        result["error"]
        == "days_per_week must be between 1 and 7"
    )


# =========================================================
# DAYS PER WEEK TOO HIGH
# =========================================================

def test_days_per_week_eight(valid_data):

    data = valid_data.copy()

    data["days_per_week"] = 8

    result = generate_workout_plan(data)

    assert "error" in result

    assert (
        result["error"]
        == "days_per_week must be between 1 and 7"
    )


# =========================================================
# INVALID DAYS PER WEEK TYPE
# =========================================================

@pytest.mark.parametrize(
    "days_per_week",
    [
        "five",
        None,
        5.5,
        True
    ]
)
def test_invalid_days_per_week_type(
    valid_data,
    days_per_week
):

    data = valid_data.copy()

    data["days_per_week"] = days_per_week

    result = generate_workout_plan(data)

    assert "error" in result


# =========================================================
# MISSING REQUIRED FIELDS
# =========================================================

@pytest.mark.parametrize(
    "field",
    [
        "goal",
        "experience_level",
        "days_per_week",
        "equipment"
    ]
)
def test_missing_required_fields(
    valid_data,
    field
):

    data = valid_data.copy()

    del data[field]

    result = generate_workout_plan(data)

    assert "error" in result

    assert (
        result["error"]
        == f"Missing required field: {field}"
    )


# =========================================================
# NONE REQUIRED FIELDS
# =========================================================

@pytest.mark.parametrize(
    "field",
    [
        "goal",
        "experience_level",
        "days_per_week",
        "equipment"
    ]
)
def test_none_required_fields(
    valid_data,
    field
):

    data = valid_data.copy()

    data[field] = None

    result = generate_workout_plan(data)

    assert "error" in result

    assert (
        result["error"]
        == f"Missing required field: {field}"
    )


# =========================================================
# NON-DICTIONARY INPUT
# =========================================================

@pytest.mark.parametrize(
    "data",
    [
        None,
        [],
        "hello",
        123
    ]
)
def test_invalid_input_object(data):

    result = generate_workout_plan(data)

    assert "error" in result


# =========================================================
# WORKOUT PLAN STRUCTURE
# =========================================================

def test_workout_plan_structure(valid_data):

    result = generate_workout_plan(valid_data)

    assert "error" not in result

    workout_plan = result["workout_plan"]

    assert isinstance(workout_plan, list)

    for workout_day in workout_plan:

        assert "day" in workout_day

        assert "focus" in workout_day

        assert "exercises" in workout_day

        assert "sets" in workout_day

        assert "repetitions" in workout_day

        assert isinstance(
            workout_day["exercises"],
            list
        )

        assert len(
            workout_day["exercises"]
        ) > 0


# =========================================================
# RECOMMENDATION EXISTS
# =========================================================

def test_workout_recommendation_exists(valid_data):

    result = generate_workout_plan(valid_data)

    assert "error" not in result

    assert "recommendation" in result

    assert isinstance(
        result["recommendation"],
        str
    )

    assert len(
        result["recommendation"]
    ) > 0