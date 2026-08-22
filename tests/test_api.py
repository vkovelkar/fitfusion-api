import requests


# =========================================================
# API CONFIGURATION
# =========================================================

BASE_URL = "http://localhost:7071"

EXECUTE_URL = f"{BASE_URL}/api/tools/execute"


# =========================================================
# TEST: FITNESS ANALYZE
# =========================================================

def test_api_fitness_analyze():

    payload = {
        "tool": "fitness.analyze",
        "arguments": {
            "name": "Vijay",
            "age": 35,
            "gender": "male",
            "weight": 72.5,
            "height": 175,
            "activity_level": "moderate",
            "goal": "fat_loss"
        }
    }

    response = requests.post(
        EXECUTE_URL,
        json=payload,
        timeout=10
    )

    assert response.status_code == 200

    data = response.json()

    assert data["tool"] == "fitness.analyze"

    assert "result" in data

    assert "analysis" in data["result"]


# =========================================================
# TEST: FITNESS RECOMMEND
# =========================================================

def test_api_fitness_recommend():

    payload = {
        "tool": "fitness.recommend",
        "arguments": {
            "goal": "fat_loss",
            "diet_preference": "vegetarian",
            "daily_calories": 2000
        }
    }

    response = requests.post(
        EXECUTE_URL,
        json=payload,
        timeout=10
    )

    assert response.status_code == 200

    data = response.json()

    assert data["tool"] == "fitness.recommend"

    assert "result" in data

    assert (
        data["result"]["goal"]
        == "fat_loss"
    )


# =========================================================
# TEST: FITNESS WORKOUT PLAN
# =========================================================

def test_api_fitness_workout_plan():

    payload = {
        "tool": "fitness.workout_plan",
        "arguments": {
            "goal": "fat_loss",
            "experience_level": "intermediate",
            "days_per_week": 5,
            "equipment": "gym"
        }
    }

    response = requests.post(
        EXECUTE_URL,
        json=payload,
        timeout=10
    )

    assert response.status_code == 200

    data = response.json()

    assert data["tool"] == "fitness.workout_plan"

    assert "result" in data

    assert "workout_plan" in data["result"]

    assert len(
        data["result"]["workout_plan"]
    ) == 5


# =========================================================
# TEST: FITNESS COMPLETE PLAN
# =========================================================

def test_api_fitness_complete_plan():

    payload = {
        "tool": "fitness.complete_plan",
        "arguments": {
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
    }

    response = requests.post(
        EXECUTE_URL,
        json=payload,
        timeout=10
    )

    assert response.status_code == 200

    data = response.json()

    assert data["tool"] == "fitness.complete_plan"

    assert "result" in data

    result = data["result"]

    assert "profile" in result

    assert "analysis" in result

    assert "nutrition_recommendations" in result

    assert "workout_plan" in result


# =========================================================
# TEST: UNKNOWN TOOL
# =========================================================

def test_api_unknown_tool():

    payload = {
        "tool": "fitness.superhuman",
        "arguments": {}
    }

    response = requests.post(
        EXECUTE_URL,
        json=payload,
        timeout=10
    )

    assert response.status_code == 404

    data = response.json()

    assert "error" in data


# =========================================================
# TEST: MISSING TOOL
# =========================================================

def test_api_missing_tool():

    payload = {
        "arguments": {}
    }

    response = requests.post(
        EXECUTE_URL,
        json=payload,
        timeout=10
    )

    assert response.status_code == 400

    data = response.json()

    assert "error" in data


# =========================================================
# TEST: MISSING ARGUMENTS
# =========================================================

def test_api_missing_arguments():

    payload = {
        "tool": "fitness.recommend"
    }

    response = requests.post(
        EXECUTE_URL,
        json=payload,
        timeout=10
    )

    assert response.status_code == 400

    data = response.json()

    assert "error" in data


# =========================================================
# TEST: INVALID TOOL ARGUMENTS
# =========================================================

def test_api_invalid_arguments():

    payload = {
        "tool": "fitness.recommend",
        "arguments": {
            "goal": "invalid_goal",
            "diet_preference": "vegetarian",
            "daily_calories": 2000
        }
    }

    response = requests.post(
        EXECUTE_URL,
        json=payload,
        timeout=10
    )

    assert response.status_code == 400

    data = response.json()

    assert "error" in data

    assert data["error"] == "Invalid goal"


# =========================================================
# TEST: INVALID REQUEST BODY
# =========================================================

def test_api_invalid_request_body():

    response = requests.post(
        EXECUTE_URL,
        json=[
            "this",
            "is",
            "not",
            "a",
            "valid",
            "request"
        ],
        timeout=10
    )

    assert response.status_code == 400

    data = response.json()

    assert "error" in data