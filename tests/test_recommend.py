import pytest

from tools.fitness.recommend import recommend_fitness


# ============================================================
# BASE VALID INPUT
# ============================================================

@pytest.fixture
def valid_data():
    return {
        "goal": "fat_loss",
        "diet_preference": "vegetarian",
        "daily_calories": 2000
    }



# ============================================================
# SUCCESS TEST
# ============================================================

def test_recommend_fitness_success(valid_data):

    result = recommend_fitness(valid_data)

    assert "error" not in result

    assert result["goal"] == "fat_loss"

    assert result["diet_preference"] == "vegetarian"

    assert result["daily_calories"] == 2000

    assert "recommendations" in result

    assert "nutrition" in result["recommendations"]

    assert "training" in result["recommendations"]

    assert "message" in result


# ============================================================
# TEST ALL VALID GOALS
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

    result = recommend_fitness(data)

    assert "error" not in result

    assert result["goal"] == goal


# ============================================================
# TEST ALL VALID DIET PREFERENCES
# ============================================================

@pytest.mark.parametrize(
    "diet_preference",
    [
        "vegetarian",
        "non_vegetarian"
    ]
)
def test_valid_diet_preferences(valid_data, diet_preference):

    data = valid_data.copy()

    data["diet_preference"] = diet_preference

    result = recommend_fitness(data)

    assert "error" not in result

    assert result["diet_preference"] == diet_preference


# ============================================================
# MISSING REQUIRED FIELDS
# ============================================================

@pytest.mark.parametrize(
    "field",
    [
        "goal",
        "diet_preference",
        "daily_calories"
    ]
)
def test_missing_required_fields(valid_data, field):

    data = valid_data.copy()

    del data[field]

    result = recommend_fitness(data)

    assert "error" in result

    assert (
        result["error"]
        ==
        f"Missing required field: {field}"
    )


# ============================================================
# INVALID GOAL
# ============================================================

def test_invalid_goal(valid_data):

    data = valid_data.copy()

    data["goal"] = "become_superhuman"

    result = recommend_fitness(data)

    assert "error" in result

    assert result["error"] == "Invalid goal"

    assert result["allowed"] == [
        "fat_loss",
        "maintenance",
        "muscle_gain"
    ]


# ============================================================
# INVALID DIET PREFERENCE
# ============================================================

def test_invalid_diet_preference(valid_data):

    data = valid_data.copy()

    data["diet_preference"] = "vegan"

    result = recommend_fitness(data)

    assert "error" in result

    assert result["error"] == "Invalid diet_preference"

    assert result["allowed"] == [
        "vegetarian",
        "non_vegetarian"
    ]


# ============================================================
# DAILY CALORIES TYPE VALIDATION
# ============================================================

@pytest.mark.parametrize(
    "value",
    [
        "two thousand",
        None,
        [],
        {}
    ]
)
def test_daily_calories_invalid_type(valid_data, value):

    data = valid_data.copy()

    data["daily_calories"] = value

    result = recommend_fitness(data)

    assert "error" in result


# ============================================================
# DAILY CALORIES RANGE VALIDATION
# ============================================================

@pytest.mark.parametrize(
    "value",
    [
        0,
        -100,
        -1
    ]
)
def test_daily_calories_must_be_positive(valid_data, value):

    data = valid_data.copy()

    data["daily_calories"] = value

    result = recommend_fitness(data)

    assert "error" in result

    assert (
        result["error"]
        ==
        "daily_calories must be greater than zero"
    )


# ============================================================
# DIFFERENT CALORIE VALUES
# ============================================================

@pytest.mark.parametrize(
    "calories",
    [
        1200,
        1800,
        2000,
        2500,
        3000
    ]
)
def test_valid_calorie_values(valid_data, calories):

    data = valid_data.copy()

    data["daily_calories"] = calories

    result = recommend_fitness(data)

    assert "error" not in result

    assert result["daily_calories"] == calories