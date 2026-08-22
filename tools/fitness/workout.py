# =========================================================
# WORKOUT PLAN TOOL
# =========================================================

from tools.validators import (
    validate_required_fields,
    validate_enum
)


# =========================================================
# ALLOWED VALUES
# =========================================================

VALID_GOALS = [
    "fat_loss",
    "maintenance",
    "muscle_gain"
]


VALID_EXPERIENCE_LEVELS = [
    "beginner",
    "intermediate",
    "advanced"
]


VALID_EQUIPMENT = [
    "gym",
    "home",
    "bodyweight"
]


# =========================================================
# WORKOUT PLAN
# =========================================================

def workout_plan(arguments):

    # =====================================================
    # STEP 1: VALIDATE INPUT OBJECT
    # =====================================================

    if not isinstance(arguments, dict):

        return {
            "error": "arguments must be an object"
        }


    # =====================================================
    # STEP 2: VALIDATE REQUIRED FIELDS
    # =====================================================
    #
    # A field is considered missing if:
    #
    # 1. The key does not exist
    # 2. The value is None
    #
    # =====================================================

    required_fields = [
        "goal",
        "experience_level",
        "days_per_week",
        "equipment"
    ]

    for field in required_fields:

        if (
            field not in arguments
            or arguments[field] is None
        ):

            return {
                "error": f"Missing required field: {field}"
            }


    # =====================================================
    # STEP 3: VALIDATE GOAL TYPE
    # =====================================================

    if not isinstance(arguments["goal"], str):

        return {
            "error": "goal must be a string",
            "allowed": VALID_GOALS
        }


    # Normalize goal

    goal = (
        arguments["goal"]
        .strip()
        .lower()
    )


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
    # STEP 5: VALIDATE EXPERIENCE LEVEL TYPE
    # =====================================================

    if not isinstance(
        arguments["experience_level"],
        str
    ):

        return {
            "error": "experience_level must be a string",
            "allowed": VALID_EXPERIENCE_LEVELS
        }


    # Normalize experience level

    experience_level = (
        arguments["experience_level"]
        .strip()
        .lower()
    )


    # =====================================================
    # STEP 6: VALIDATE EXPERIENCE LEVEL
    # =====================================================

    error = validate_enum(
        experience_level,
        "experience_level",
        VALID_EXPERIENCE_LEVELS
    )

    if error:

        return error


    # =====================================================
    # STEP 7: VALIDATE DAYS PER WEEK TYPE
    # =====================================================
    #
    # bool must be checked explicitly because:
    #
    # isinstance(True, int)
    #
    # returns True in Python.
    #
    # =====================================================

    days_per_week = arguments["days_per_week"]

    if (
        not isinstance(days_per_week, int)
        or isinstance(days_per_week, bool)
    ):

        return {
            "error": "days_per_week must be an integer"
        }


    # =====================================================
    # STEP 8: VALIDATE DAYS PER WEEK RANGE
    # =====================================================

    if (
        days_per_week < 1
        or days_per_week > 7
    ):

        return {
            "error": (
                "days_per_week must be between 1 and 7"
            )
        }


    # =====================================================
    # STEP 9: VALIDATE EQUIPMENT TYPE
    # =====================================================

    if not isinstance(
        arguments["equipment"],
        str
    ):

        return {
            "error": "equipment must be a string",
            "allowed": VALID_EQUIPMENT
        }


    # Normalize equipment

    equipment = (
        arguments["equipment"]
        .strip()
        .lower()
    )


    # =====================================================
    # STEP 10: VALIDATE EQUIPMENT
    # =====================================================

    error = validate_enum(
        equipment,
        "equipment",
        VALID_EQUIPMENT
    )

    if error:

        return error


    # =====================================================
    # WORKOUT TEMPLATES
    # =====================================================

    if days_per_week == 1:

        workout_plan_data = [
            {
                "day": "Day 1",
                "focus": "Full Body",
                "exercises": [
                    "Squats",
                    "Bench Press",
                    "Lat Pulldown",
                    "Shoulder Press",
                    "Plank"
                ]
            }
        ]


    elif days_per_week == 2:

        workout_plan_data = [
            {
                "day": "Day 1",
                "focus": "Upper Body",
                "exercises": [
                    "Bench Press",
                    "Lat Pulldown",
                    "Shoulder Press",
                    "Seated Row",
                    "Bicep Curls"
                ]
            },
            {
                "day": "Day 2",
                "focus": "Lower Body",
                "exercises": [
                    "Squats",
                    "Romanian Deadlift",
                    "Leg Press",
                    "Walking Lunges",
                    "Calf Raises"
                ]
            }
        ]


    else:

        workout_plan_data = [

    {
        "day": "Day 1",
        "focus": "Upper Body",
        "exercises": [
            "Bench Press",
            "Lat Pulldown",
            "Shoulder Press",
            "Seated Row",
            "Bicep Curls"
        ]
    },

    {
        "day": "Day 2",
        "focus": "Lower Body",
        "exercises": [
            "Squats",
            "Romanian Deadlift",
            "Leg Press",
            "Walking Lunges",
            "Calf Raises"
        ]
    },

    {
        "day": "Day 3",
        "focus": "Push",
        "exercises": [
            "Bench Press",
            "Incline Dumbbell Press",
            "Shoulder Press",
            "Lateral Raises",
            "Tricep Pushdown"
        ]
    },

    {
        "day": "Day 4",
        "focus": "Pull",
        "exercises": [
            "Deadlift",
            "Lat Pulldown",
            "Barbell Row",
            "Face Pull",
            "Bicep Curls"
        ]
    },

    {
        "day": "Day 5",
        "focus": "Legs and Core",
        "exercises": [
            "Squats",
            "Leg Curl",
            "Leg Extension",
            "Plank",
            "Hanging Leg Raises"
        ]
    },

    {
        "day": "Day 6",
        "focus": "Full Body",
        "exercises": [
            "Goblet Squats",
            "Dumbbell Bench Press",
            "Seated Row",
            "Romanian Deadlift",
            "Plank"
        ]
    },

    {
        "day": "Day 7",
        "focus": "Active Recovery",
        "exercises": [
            "Walking",
            "Light Cycling",
            "Mobility Exercises",
            "Stretching",
            "Foam Rolling"
        ]
    }
]

        # Return only the requested number of days.
        workout_plan_data = workout_plan_data[
            :days_per_week
        ]


    # =====================================================
    # ADJUSTMENT FOR EXPERIENCE LEVEL
    # =====================================================

    if experience_level == "beginner":

        sets = 2
        repetitions = "8-10"

    elif experience_level == "advanced":

        sets = 4
        repetitions = "8-15"

    else:

        sets = 3
        repetitions = "8-12"


    # =====================================================
    # ADD SETS AND REPETITIONS
    # =====================================================

    for workout_day in workout_plan_data:

        workout_day["sets"] = sets

        workout_day["repetitions"] = repetitions


    # =====================================================
    # FINAL RESPONSE
    # =====================================================

    return {

        "goal": goal,

        "experience_level": experience_level,

        "days_per_week": days_per_week,

        "equipment": equipment,

        "workout_plan": workout_plan_data,

        "recommendation": (
            "Focus on progressive overload, proper form, "
            "adequate recovery, and consistency."
        )
    }


# =========================================================
# BACKWARD-COMPATIBLE FUNCTION NAME
# =========================================================
#
# Your tests import generate_workout_plan.
# Keep this wrapper so the rest of the project continues
# working without changing every import.
# =========================================================

def generate_workout_plan(data):

    return workout_plan(data)