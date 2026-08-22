# =========================================================
# FITNESS ANALYSIS TOOL
# =========================================================
#
# This tool:
#
# 1. Validates a user's fitness profile
# 2. Calculates BMI
# 3. Calculates BMR
# 4. Estimates maintenance calories
# 5. Calculates goal-based target calories
# 6. Calculates macronutrient targets
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
    validate_string,
    validate_number_range,
    validate_enum
)


# =========================================================
# ALLOWED VALUES
# =========================================================
#
# These are the values supported specifically by this tool.
#
# The shared validator does not know what values are valid
# for "goal" or "activity_level".
#
# The tool itself defines those business rules.
# =========================================================

VALID_GENDERS = [
    "male",
    "female"
]

VALID_ACTIVITY_LEVELS = [
    "sedentary",
    "light",
    "moderate",
    "active",
    "very_active"
]

VALID_GOALS = [
    "fat_loss",
    "maintenance",
    "muscle_gain"
]


# =========================================================
# FITNESS ANALYSIS
# =========================================================

def analyze_fitness(data):

    # =====================================================
    # STEP 1: VALIDATE REQUIRED FIELDS
    # =====================================================

    required_fields = [
        "name",
        "age",
        "gender",
        "weight",
        "height",
        "activity_level",
        "goal"
    ]

    error = validate_required_fields(
        data,
        required_fields
    )

    if error:
        return error


    # =====================================================
    # STEP 2: VALIDATE NAME
    # =====================================================

    error = validate_string(
        data["name"],
        "name"
    )

    if error:
        return error


    # =====================================================
    # STEP 3: VALIDATE AGE
    # =====================================================

    error = validate_number_range(
        data["age"],
        "age",
        1,
        120
    )

    if error:
        return error


    # =====================================================
    # STEP 4: VALIDATE GENDER
    # =====================================================

    error = validate_enum(
        data["gender"],
        "gender",
        VALID_GENDERS
    )

    if error:
        return error


    # =====================================================
    # STEP 5: VALIDATE WEIGHT
    # =====================================================

    error = validate_number_range(
        data["weight"],
        "weight",
        1,
        500
    )

    if error:
        return error


    # =====================================================
    # STEP 6: VALIDATE HEIGHT
    # =====================================================

    error = validate_number_range(
        data["height"],
        "height",
        1,
        300
    )

    if error:
        return error


    # =====================================================
    # STEP 7: VALIDATE ACTIVITY LEVEL
    # =====================================================

    error = validate_enum(
        data["activity_level"],
        "activity_level",
        VALID_ACTIVITY_LEVELS
    )

    if error:
        return error


    # =====================================================
    # STEP 8: VALIDATE GOAL
    # =====================================================

    error = validate_enum(
        data["goal"],
        "goal",
        VALID_GOALS
    )

    if error:
        return error


    # =====================================================
    # INPUT IS NOW VALID
    # =====================================================

    name = data["name"].strip()
    age = data["age"]
    gender = data["gender"]
    weight = data["weight"]
    height = data["height"]
    activity_level = data["activity_level"]
    goal = data["goal"]


    # =====================================================
    # BMI CALCULATION
    # =====================================================

    height_m = height / 100

    bmi = round(
        weight / (height_m ** 2),
        2
    )


    # =====================================================
    # BMI CATEGORY
    # =====================================================

    if bmi < 18.5:
        bmi_category = "underweight"

    elif bmi < 25:
        bmi_category = "normal"

    elif bmi < 30:
        bmi_category = "overweight"

    else:
        bmi_category = "obese"


    # =====================================================
    # BMR CALCULATION
    # Mifflin-St Jeor Equation
    # =====================================================

    if gender == "male":

        bmr = round(
            (10 * weight)
            + (6.25 * height)
            - (5 * age)
            + 5
        )

    else:

        bmr = round(
            (10 * weight)
            + (6.25 * height)
            - (5 * age)
            - 161
        )


    # =====================================================
    # ACTIVITY MULTIPLIERS
    # =====================================================

    activity_multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9
    }


    # =====================================================
    # MAINTENANCE CALORIES
    # =====================================================

    maintenance_calories = round(
        bmr * activity_multipliers[activity_level]
    )


    # =====================================================
    # GOAL-BASED CALORIE TARGET
    # =====================================================

    if goal == "fat_loss":

        target_calories = round(
            maintenance_calories * 0.80
        )

        protein_target = round(
            weight * 2.0
        )

        fat_target = round(
            weight * 0.8
        )

    elif goal == "muscle_gain":

        target_calories = round(
            maintenance_calories * 1.10
        )

        protein_target = round(
            weight * 2.0
        )

        fat_target = round(
            weight * 1.0
        )

    else:

        target_calories = maintenance_calories

        protein_target = round(
            weight * 1.6
        )

        fat_target = round(
            weight * 0.9
        )


    # =====================================================
    # CARBOHYDRATE CALCULATION
    # =====================================================
    #
    # Protein = 4 calories per gram
    # Fat = 9 calories per gram
    # Carbohydrates = remaining calories / 4
    # =====================================================

    protein_calories = protein_target * 4
    fat_calories = fat_target * 9

    remaining_calories = (
        target_calories
        - protein_calories
        - fat_calories
    )

    carbohydrates_target = round(
        max(0, remaining_calories) / 4
    )


    # =====================================================
    # GOAL-BASED RECOMMENDATION
    # =====================================================

    if goal == "fat_loss":

        recommendation = (
            "Maintain a moderate calorie deficit, prioritize "
            "high protein intake, perform regular strength "
            "training, and monitor your progress weekly."
        )

    elif goal == "muscle_gain":

        recommendation = (
            "Maintain a moderate calorie surplus, prioritize "
            "progressive overload, consume sufficient protein, "
            "and support recovery with adequate sleep."
        )

    else:

        recommendation = (
            "Maintain balanced nutrition, regular exercise, "
            "sufficient protein intake, and monitor your body "
            "composition over time."
        )


    # =====================================================
    # FINAL RESPONSE
    # =====================================================

    return {

        "name": name,

        "profile": {
            "age": age,
            "gender": gender,
            "weight_kg": weight,
            "height_cm": height,
            "activity_level": activity_level,
            "goal": goal
        },

        "analysis": {
            "bmi": bmi,
            "bmi_category": bmi_category,
            "bmr_calories": bmr,
            "maintenance_calories": maintenance_calories,
            "target_calories": target_calories,

            "macros": {
                "protein_g": protein_target,
                "fat_g": fat_target,
                "carbohydrates_g": carbohydrates_target
            },

            "recommendation": recommendation
        },

        "message": "Fitness profile analyzed successfully"
    }