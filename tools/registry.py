TOOLS = {

    "fitness.analyze": {
        "name": "fitness.analyze",

        "description": (
            "Analyzes a user's fitness profile and returns BMI, "
            "BMR, calorie targets, macronutrient targets, and "
            "goal-based recommendations."
        ),

        "input_schema": {
            "type": "object",

            "required": [
                "name",
                "age",
                "gender",
                "weight",
                "height",
                "activity_level",
                "goal"
            ],

            "properties": {

                "name": {
                    "type": "string"
                },

                "age": {
                    "type": "number"
                },

                "gender": {
                    "type": "string",
                    "enum": [
                        "male",
                        "female"
                    ]
                },

                "weight": {
                    "type": "number",
                    "description": "Weight in kilograms"
                },

                "height": {
                    "type": "number",
                    "description": "Height in centimeters"
                },

                "activity_level": {
                    "type": "string",
                    "enum": [
                        "sedentary",
                        "light",
                        "moderate",
                        "active",
                        "very_active"
                    ]
                },

                "goal": {
                    "type": "string",
                    "enum": [
                        "fat_loss",
                        "maintenance",
                        "muscle_gain"
                    ]
                }
            }
        }
    },


    "fitness.recommend": {
        "name": "fitness.recommend",

        "description": (
            "Generates personalized nutrition and training "
            "recommendations based on a user's fitness goal, "
            "diet preference, and daily calorie target."
        ),

        "input_schema": {
            "type": "object",

            "required": [
                "goal",
                "diet_preference",
                "daily_calories"
            ],

            "properties": {

                "goal": {
                    "type": "string",
                    "enum": [
                        "fat_loss",
                        "maintenance",
                        "muscle_gain"
                    ]
                },

                "diet_preference": {
                    "type": "string",
                    "enum": [
                        "vegetarian",
                        "non_vegetarian"
                    ]
                },

                "daily_calories": {
                    "type": "number",
                    "description": "Target daily calorie intake"
                }
            }
        }
    },


    "fitness.workout_plan": {
        "name": "fitness.workout_plan",

        "description": (
            "Generates a workout plan based on fitness goal, "
            "experience level, training days, and equipment."
        ),

        "input_schema": {
            "type": "object",

            "required": [
                "goal",
                "experience_level",
                "days_per_week",
                "equipment"
            ],

            "properties": {

                "goal": {
                    "type": "string",
                    "enum": [
                        "fat_loss",
                        "muscle_gain",
                        "maintenance"
                    ]
                },

                "experience_level": {
                    "type": "string",
                    "enum": [
                        "beginner",
                        "intermediate",
                        "advanced"
                    ]
                },

                "days_per_week": {
                    "type": "number"
                },

                "equipment": {
                    "type": "string",
                    "enum": [
                        "gym",
                        "home",
                        "bodyweight"
                    ]
                }
            }
        }
    },


    "fitness.complete_plan": {
        "name": "fitness.complete_plan",

        "description": (
            "Generates a complete personalized fitness plan by combining "
            "fitness analysis, nutrition recommendations, and a workout plan."
        ),

        "input_schema": {
            "type": "object",

            "required": [
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
            ],

            "properties": {

                "name": {
                    "type": "string"
                },

                "age": {
                    "type": "number"
                },

                "gender": {
                    "type": "string",
                    "enum": [
                        "male",
                        "female"
                    ]
                },

                "weight": {
                    "type": "number",
                    "description": "Weight in kilograms"
                },

                "height": {
                    "type": "number",
                    "description": "Height in centimeters"
                },

                "activity_level": {
                    "type": "string",
                    "enum": [
                        "sedentary",
                        "light",
                        "moderate",
                        "active",
                        "very_active"
                    ]
                },

                "goal": {
                    "type": "string",
                    "enum": [
                        "fat_loss",
                        "maintenance",
                        "muscle_gain"
                    ]
                },

                "diet_preference": {
                    "type": "string",
                    "enum": [
                        "vegetarian",
                        "non_vegetarian"
                    ]
                },

                "experience_level": {
                    "type": "string",
                    "enum": [
                        "beginner",
                        "intermediate",
                        "advanced"
                    ]
                },

                "days_per_week": {
                    "type": "number"
                },

                "equipment": {
                    "type": "string",
                    "enum": [
                        "gym",
                        "home",
                        "bodyweight"
                    ]
                }
            }
        }
    },


    "fitness.predict_calories": {
        "name": "fitness.predict_calories",

        "description": (
            "Predicts calories burned during a workout using a "
            "trained machine learning model."
        ),

        "input_schema": {
            "type": "object",

            "required": [
                "age",
                "weight",
                "height",
                "duration",
                "heart_rate",
                "workout_type"
            ],

            "properties": {

                "age": {
                    "type": "number",
                    "description": "Age in years"
                },

                "weight": {
                    "type": "number",
                    "description": "Weight in kilograms"
                },

                "height": {
                    "type": "number",
                    "description": "Height in centimeters"
                },

                "duration": {
                    "type": "number",
                    "description": "Workout duration in minutes"
                },

                "heart_rate": {
                    "type": "number",
                    "description": "Average heart rate during workout"
                },

                "workout_type": {
                    "type": "string",
                    "enum": [
                        "Running",
                        "Cycling",
                        "Walking",
                        "Yoga"
                    ]
                }
            }
        }
    }
}