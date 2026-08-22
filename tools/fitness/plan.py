# ============================================================
# FITFUSION COMPLETE FITNESS PLAN
# ============================================================
#
# This file is the orchestration layer for the FitFusion API.
#
# It validates ALL input required for a complete fitness plan
# before calling the individual fitness tools.
#
# Flow:
#
#     User Request
#          |
#          v
#     Validate Complete Input
#          |
#          v
#     Fitness Analysis
#          |
#          v
#     Nutrition Recommendation
#          |
#          v
#     Workout Plan
#          |
#          v
#     Complete Fitness Plan
#
# ============================================================


from .analyze import analyze_fitness
from .recommend import recommend_fitness
from .workout import workout_plan as generate_workout_plan


# ============================================================
# VALIDATION FUNCTION
# ============================================================

def validate_complete_plan_input(data):
    """
    Validates all fields required by fitness.complete_plan.

    Returns:
        None if validation succeeds.

        Dictionary containing an error message if validation fails.
    """

    # --------------------------------------------------------
    # CHECK THAT INPUT IS A DICTIONARY
    # --------------------------------------------------------

    if not isinstance(data, dict):
        return {
            "error": "arguments must be a JSON object"
        }

    # --------------------------------------------------------
    # REQUIRED FIELDS
    # --------------------------------------------------------

    required_fields = [
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

    # Check whether any required fields are missing.
    for field in required_fields:

        if field not in data:

            return {
                "error": f"Missing required field: {field}"
            }

    # ========================================================
    # NAME VALIDATION
    # ========================================================

    name = data["name"]

    if not isinstance(name, str):

        return {
            "error": "name must be a string"
        }

    if not name.strip():

        return {
            "error": "name cannot be empty"
        }

    # ========================================================
    # AGE VALIDATION
    # ========================================================

    age = data["age"]

    # bool is technically an int in Python,
    # so explicitly reject it.
    if isinstance(age, bool) or not isinstance(age, int):

        return {
            "error": "age must be an integer"
        }

    if age <= 0:

        return {
            "error": "age must be greater than zero"
        }

    # ========================================================
    # GENDER VALIDATION
    # ========================================================

    gender = data["gender"]

    if not isinstance(gender, str):

        return {
            "error": "gender must be a string"
        }

    allowed_genders = [
        "male",
        "female"
    ]

    if gender.lower() not in allowed_genders:

        return {
            "error": "Invalid gender",
            "allowed": allowed_genders
        }

    # ========================================================
    # WEIGHT VALIDATION
    # ========================================================

    weight = data["weight"]

    if isinstance(weight, bool) or not isinstance(
        weight,
        (int, float)
    ):

        return {
            "error": "weight must be a number"
        }

    if weight <= 0:

        return {
            "error": "weight must be greater than zero"
        }

    # ========================================================
    # HEIGHT VALIDATION
    # ========================================================

    height = data["height"]

    if isinstance(height, bool) or not isinstance(
        height,
        (int, float)
    ):

        return {
            "error": "height must be a number"
        }

    if height <= 0:

        return {
            "error": "height must be greater than zero"
        }

    # ========================================================
    # ACTIVITY LEVEL VALIDATION
    # ========================================================

    activity_level = data["activity_level"]

    if not isinstance(activity_level, str):

        return {
            "error": "activity_level must be a string"
        }

    allowed_activity_levels = [
        "sedentary",
        "light",
        "moderate",
        "active",
        "very_active"
    ]

    if activity_level.lower() not in allowed_activity_levels:

        return {
            "error": "Invalid activity_level",
            "allowed": allowed_activity_levels
        }

    # ========================================================
    # GOAL VALIDATION
    # ========================================================

    goal = data["goal"]

    if not isinstance(goal, str):

        return {
            "error": "goal must be a string",
            "allowed": [
                "fat_loss",
                "maintenance",
                "muscle_gain"
            ]
        }

    allowed_goals = [
        "fat_loss",
        "maintenance",
        "muscle_gain"
    ]

    if goal.lower() not in allowed_goals:

        return {
            "error": "Invalid goal",
            "allowed": allowed_goals
        }

    # ========================================================
    # DIET PREFERENCE VALIDATION
    # ========================================================

    diet_preference = data["diet_preference"]

    if not isinstance(diet_preference, str):

        return {
            "error": "diet_preference must be a string",
            "allowed": [
                "vegetarian",
                "non_vegetarian"
            ]
        }

    allowed_diet_preferences = [
        "vegetarian",
        "non_vegetarian"
    ]

    if diet_preference.lower() not in allowed_diet_preferences:

        return {
            "error": "Invalid diet_preference",
            "allowed": allowed_diet_preferences
        }

    # ========================================================
    # EXPERIENCE LEVEL VALIDATION
    # ========================================================

    experience_level = data["experience_level"]

    if not isinstance(experience_level, str):

        return {
            "error": "experience_level must be a string",
            "allowed": [
                "beginner",
                "intermediate",
                "advanced"
            ]
        }

    allowed_experience_levels = [
        "beginner",
        "intermediate",
        "advanced"
    ]

    if experience_level.lower() not in allowed_experience_levels:

        return {
            "error": "Invalid experience_level",
            "allowed": allowed_experience_levels
        }

    # ========================================================
    # DAYS PER WEEK VALIDATION
    # ========================================================

    days_per_week = data["days_per_week"]

    if isinstance(days_per_week, bool) or not isinstance(
        days_per_week,
        int
    ):

        return {
            "error": "days_per_week must be an integer"
        }

    if days_per_week < 1 or days_per_week > 7:

        return {
            "error": "days_per_week must be between 1 and 7"
        }

    # ========================================================
    # EQUIPMENT VALIDATION
    # ========================================================

    equipment = data["equipment"]

    if not isinstance(equipment, str):

        return {
            "error": "equipment must be a string",
            "allowed": [
                "gym",
                "home",
                "bodyweight"
            ]
        }

    allowed_equipment = [
        "gym",
        "home",
        "bodyweight"
    ]

    if equipment.lower() not in allowed_equipment:

        return {
            "error": "Invalid equipment",
            "allowed": allowed_equipment
        }

    # --------------------------------------------------------
    # ALL VALIDATION PASSED
    # --------------------------------------------------------

    return None


# ============================================================
# COMPLETE FITNESS PLAN
# ============================================================

def generate_complete_plan(data):
    """
    Generates a complete fitness plan.

    The function first validates all user input.

    If validation succeeds, it orchestrates:

        1. Fitness analysis
        2. Nutrition recommendation
        3. Workout plan

    Returns one combined response.
    """

    # ========================================================
    # STEP 1: VALIDATE THE COMPLETE REQUEST
    # ========================================================

    validation_error = validate_complete_plan_input(data)

    if validation_error:

        return validation_error

    # ========================================================
    # STEP 2: NORMALIZE STRING INPUT
    # ========================================================
    #
    # This allows values such as:
    #
    # "FAT_LOSS"
    # "Fat_Loss"
    # "fat_loss"
    #
    # to be processed consistently.
    #

    normalized_data = data.copy()

    normalized_data["name"] = data["name"].strip()

    normalized_data["gender"] = data["gender"].lower()

    normalized_data["activity_level"] = (
        data["activity_level"].lower()
    )

    normalized_data["goal"] = data["goal"].lower()

    normalized_data["diet_preference"] = (
        data["diet_preference"].lower()
    )

    normalized_data["experience_level"] = (
        data["experience_level"].lower()
    )

    normalized_data["equipment"] = (
        data["equipment"].lower()
    )

    # ========================================================
    # STEP 3: ANALYZE FITNESS PROFILE
    # ========================================================

    analysis_result = analyze_fitness(
        normalized_data
    )

    # Defensive check.
    # Individual tools should not return errors after complete
    # validation, but this prevents a false success response.

    if "error" in analysis_result:

        return analysis_result

    # ========================================================
    # STEP 4: EXTRACT SHARED VALUES
    # ========================================================

    goal = normalized_data["goal"]

    target_calories = (
        analysis_result["analysis"]
        ["target_calories"]
    )

    # ========================================================
    # STEP 5: GET NUTRITION RECOMMENDATIONS
    # ========================================================

    nutrition_result = recommend_fitness({
        "goal": goal,
        "diet_preference": (
            normalized_data["diet_preference"]
        ),
        "daily_calories": target_calories
    })

    # Stop immediately if nutrition generation fails.

    if "error" in nutrition_result:

        return nutrition_result

    # ========================================================
    # STEP 6: GENERATE WORKOUT PLAN
    # ========================================================

    workout_result = generate_workout_plan({
        "goal": goal,
        "experience_level": (
            normalized_data["experience_level"]
        ),
        "days_per_week": (
            normalized_data["days_per_week"]
        ),
        "equipment": (
            normalized_data["equipment"]
        )
    })

    # Stop immediately if workout generation fails.

    if "error" in workout_result:

        return workout_result

    # ========================================================
    # STEP 7: COMBINE ALL RESULTS
    # ========================================================

    return {
        "profile": analysis_result["profile"],

        "analysis": analysis_result["analysis"],

        "nutrition_recommendations": nutrition_result,

        "workout_plan": workout_result
    }