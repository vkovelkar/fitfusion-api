# =========================================================
# FITNESS RECOMMENDATION TOOL
# =========================================================
#
# This tool:
#
# 1. Validates recommendation input
# 2. Validates the user's fitness goal
# 3. Validates diet preference
# 4. Validates daily calorie input
# 5. Generates training recommendations
# 6. Generates nutrition recommendations
#
# Common validation logic is imported from:
#
# tools/validators.py
#
# =========================================================


# =========================================================
# IMPORT SHARED VALIDATORS
# =========================================================

from tools.validators import (
    validate_required_fields,
    validate_enum,
    validate_positive_number
)


# =========================================================
# ALLOWED VALUES
# =========================================================
#
# These are business rules specific to this recommendation
# tool.
#
# The shared validators know HOW to validate.
# This file defines WHAT values are valid.
# =========================================================

VALID_GOALS = [
    "fat_loss",
    "maintenance",
    "muscle_gain"
]


VALID_DIET_PREFERENCES = [
    "vegetarian",
    "non_vegetarian"
]


# =========================================================
# FITNESS RECOMMENDATION
# =========================================================
#
# This function is called by:
#
# router.py
#     ↓
# execute_tool()
#     ↓
# recommend_fitness(data)
#
# =========================================================

def recommend_fitness(data):

    # =====================================================
    # STEP 1: VALIDATE INPUT OBJECT
    # =====================================================
    #
    # The function expects a dictionary.
    #
    # This prevents errors if invalid data such as:
    #
    # None
    # []
    # "hello"
    # 123
    #
    # is passed to the function.
    # =====================================================

    if not isinstance(data, dict):

        return {
            "error": "arguments must be an object"
        }


    # =====================================================
    # STEP 2: VALIDATE REQUIRED FIELDS
    # =====================================================
    #
    # All three values are required before we can generate
    # recommendations.
    # =====================================================

    required_fields = [
        "goal",
        "diet_preference",
        "daily_calories"
    ]

    error = validate_required_fields(
        data,
        required_fields
    )

    if error:
        return error


    # =====================================================
    # STEP 3: VALIDATE GOAL TYPE
    # =====================================================
    #
    # We MUST check that goal is a string BEFORE calling:
    #
    # .lower()
    #
    # Otherwise an integer such as:
    #
    # "goal": 123
    #
    # would cause:
    #
    # AttributeError:
    # 'int' object has no attribute 'lower'
    # =====================================================

    if not isinstance(data["goal"], str):

        return {
            "error": "goal must be a string",
            "allowed": VALID_GOALS
        }


    # Remove unnecessary spaces and normalize case.
    #
    # Examples:
    #
    # " FAT_LOSS "
    # "Fat_Loss"
    # "fat_loss"
    #
    # All become:
    #
    # "fat_loss"

    goal = data["goal"].strip().lower()


    # =====================================================
    # STEP 4: VALIDATE GOAL VALUE
    # =====================================================

    error = validate_enum(
        goal,
        "goal",
        VALID_GOALS
    )

    if error:
        return error


    # =====================================================
    # STEP 5: VALIDATE DIET PREFERENCE TYPE
    # =====================================================
    #
    # Check type BEFORE calling:
    #
    # .lower()
    #
    # =====================================================

    if not isinstance(data["diet_preference"], str):

        return {
            "error": "diet_preference must be a string",
            "allowed": VALID_DIET_PREFERENCES
        }


    # Normalize diet preference.
    #
    # Examples:
    #
    # "VEGETARIAN"
    # " Vegetarian "
    # "vegetarian"
    #
    # All become:
    #
    # "vegetarian"

    diet_preference = (
        data["diet_preference"]
        .strip()
        .lower()
    )


    # =====================================================
    # STEP 6: VALIDATE DIET PREFERENCE VALUE
    # =====================================================

    error = validate_enum(
        diet_preference,
        "diet_preference",
        VALID_DIET_PREFERENCES
    )

    if error:
        return error


    # =====================================================
    # STEP 7: VALIDATE DAILY CALORIES
    # =====================================================
    #
    # daily_calories must be:
    #
    # - A number
    # - Greater than zero
    #
    # Examples of invalid values:
    #
    # 0
    # -500
    # True
    # False
    # "two thousand"
    #
    # =====================================================

    error = validate_positive_number(
        data["daily_calories"],
        "daily_calories"
    )

    if error:
        return error


    # =====================================================
    # INPUT IS VALID
    # =====================================================

    daily_calories = float(
        data["daily_calories"]
    )


    # =====================================================
    # GOAL-BASED TRAINING RECOMMENDATION
    # =====================================================

    if goal == "fat_loss":

        training_recommendation = (
            "Focus on strength training 3 to 5 times per week, "
            "maintain a calorie deficit, and include regular cardio."
        )


    elif goal == "muscle_gain":

        training_recommendation = (
            "Focus on progressive overload, train major muscle groups "
            "consistently, and support recovery with adequate sleep."
        )


    else:

        # The only remaining valid goal is "maintenance".

        training_recommendation = (
            "Follow a balanced training routine with strength training, "
            "cardiovascular exercise, and adequate recovery."
        )


    # =====================================================
    # DIET-BASED NUTRITION RECOMMENDATION
    # =====================================================

    if diet_preference == "vegetarian":

        nutrition_recommendation = (
            "Prioritize protein sources such as paneer, tofu, Greek yogurt, "
            "lentils, beans, soy, and other high-protein vegetarian foods."
        )


    else:

        # The only remaining valid preference is:
        # "non_vegetarian"

        nutrition_recommendation = (
            "Prioritize lean protein sources such as chicken, fish, eggs, "
            "Greek yogurt, and other minimally processed protein sources."
        )


    # =====================================================
    # FINAL RESPONSE
    # =====================================================
    #
    # This result is returned to router.py.
    #
    # function_app.py wraps it as:
    #
    # {
    #     "tool": "fitness.recommend",
    #     "result": {
    #         ...
    #     }
    # }
    #
    # =====================================================

    return {

        "goal": goal,

        "diet_preference": diet_preference,

        "daily_calories": round(
            daily_calories
        ),

        "recommendations": {

            "nutrition": nutrition_recommendation,

            "training": training_recommendation
        },

        "message": (
            "Fitness recommendations generated successfully"
        )
    }