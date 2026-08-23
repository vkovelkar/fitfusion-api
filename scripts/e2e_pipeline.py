import json
import sys
import requests

BASE_URL = "http://localhost:8080"


def print_header(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60 + "\n")


def print_response(response):
    print(f"Status Code: {response.status_code}")

    try:
        print("Response:")
        print(json.dumps(response.json(), indent=2))
    except Exception:
        print("Response:")
        print(response.text)


def validate_response(response, expected_status=200):
    if response.status_code == expected_status:
        print("\nSUCCESS")
        return True

    print(
        f"\nFAILED: Expected {expected_status}, "
        f"got {response.status_code}"
    )
    return False


def main():

    print("\nFITFUSION END-TO-END PIPELINE")
    print(f"Target: {BASE_URL}")

    # ============================================================
    # STEP 1: HEALTH CHECK
    # ============================================================

    print_header("STEP 1: HEALTH CHECK")

    response = requests.get(
        f"{BASE_URL}/api/health",
        timeout=30
    )

    print_response(response)

    if not validate_response(response):
        sys.exit(1)

    # ============================================================
    # STEP 2: LIST AVAILABLE TOOLS
    # ============================================================

    print_header("STEP 2: LIST AVAILABLE TOOLS")

    response = requests.get(
        f"{BASE_URL}/api/tools",
        timeout=30
    )

    print_response(response)

    if not validate_response(response):
        sys.exit(1)

    # ============================================================
    # STEP 3: FITNESS ANALYSIS
    # ============================================================

    print_header("STEP 3: FITNESS ANALYSIS")

    analyze_payload = {
        "name": "Vijay",
        "age": 35,
        "gender": "male",
        "weight": 72,
        "height": 175,
        "activity_level": "moderate",
        "goal": "fat_loss"
    }

    response = requests.post(
        f"{BASE_URL}/api/fitness/analyze",
        json=analyze_payload,
        timeout=30
    )

    print_response(response)

    if not validate_response(response):
        sys.exit(1)

    analysis_result = response.json()

    target_calories = analysis_result["analysis"]["target_calories"]

    print(f"\nTarget Calories from analysis: {target_calories}")

    # ============================================================
    # STEP 4: NUTRITION RECOMMENDATION
    # ============================================================

    print_header("STEP 4: NUTRITION RECOMMENDATION")

    recommend_payload = {
        "tool": "fitness.recommend",
        "arguments": {
            "goal": "fat_loss",
            "diet_preference": "non_vegetarian",
            "daily_calories": target_calories
        }
    }

    response = requests.post(
        f"{BASE_URL}/api/tools/execute",
        json=recommend_payload,
        timeout=30
    )

    print_response(response)

    if not validate_response(response):
        sys.exit(1)

    # ============================================================
    # STEP 5: WORKOUT PLAN
    # ============================================================

    print_header("STEP 5: WORKOUT PLAN")

    workout_payload = {
        "tool": "fitness.workout_plan",
        "arguments": {
            "goal": "fat_loss",
            "experience_level": "intermediate",
            "days_per_week": 5,
            "equipment": "gym"
        }
    }

    response = requests.post(
        f"{BASE_URL}/api/tools/execute",
        json=workout_payload,
        timeout=30
    )

    print_response(response)

    if not validate_response(response):
        sys.exit(1)

    # ============================================================
    # STEP 6: COMPLETE FITNESS PLAN
    # ============================================================

    print_header("STEP 6: COMPLETE FITNESS PLAN")

    complete_plan_payload = {
        "tool": "fitness.complete_plan",
        "arguments": {
            "name": "Vijay",
            "age": 35,
            "gender": "male",
            "weight": 72,
            "height": 175,
            "activity_level": "moderate",
            "goal": "fat_loss",
            "diet_preference": "non_vegetarian",
            "experience_level": "intermediate",
            "days_per_week": 5,
            "equipment": "gym"
        }
    }

    response = requests.post(
        f"{BASE_URL}/api/tools/execute",
        json=complete_plan_payload,
        timeout=30
    )

    print_response(response)

    if not validate_response(response):
        sys.exit(1)

    # ============================================================
    # PIPELINE COMPLETED
    # ============================================================

    print_header("FITFUSION END-TO-END PIPELINE COMPLETED")

    print("ALL TESTS PASSED SUCCESSFULLY")
    print("\nVerified:")
    print("✓ Kubernetes service connectivity")
    print("✓ Health endpoint")
    print("✓ Tool discovery")
    print("✓ Fitness analysis")
    print("✓ Nutrition recommendation")
    print("✓ Workout plan")
    print("✓ Complete fitness plan")


if __name__ == "__main__":
    main()