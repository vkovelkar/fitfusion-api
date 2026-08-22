# FitFusion API

FitFusion is a modular fitness planning API built with Python and Azure Functions.

The API analyzes a user's fitness profile and generates personalized nutrition recommendations, training recommendations, workout plans, and complete fitness plans.

The project uses a modular tool-based architecture where individual fitness capabilities are registered and executed through a central router.

---

# Features

FitFusion currently provides four fitness tools:

- `fitness.analyze`
- `fitness.recommend`
- `fitness.workout_plan`
- `fitness.complete_plan`

The API supports:

- Fitness profile analysis
- BMI calculation
- BMI category classification
- BMR calculation
- Maintenance calorie estimation
- Target calorie calculation
- Macronutrient recommendations
- Goal-based nutrition recommendations
- Goal-based training recommendations
- Workout plan generation
- Complete fitness plan orchestration
- Shared input validation
- API-level error handling
- Automated testing

---

# Architecture

```text
Client
   |
   v
Azure Function API
   |
   v
Router
   |
   v
Tool Registry
   |
   +-----------------------------------+
   |              |                    |
   v              v                    v
fitness.analyze   fitness.recommend    fitness.workout_plan
   |              |                    |
   v              v                    v
Profile Analysis  Nutrition + Training Workout Generator
   \              |                    /
    \             |                   /
     +------------+------------------+
                  |
                  v
        fitness.complete_plan
                  |
                  v
          Complete Fitness Plan
```

---

# Project Structure

```text
fitfusion-api/
│
├── function_app.py
├── router.py
├── registry.py
├── requirements.txt
├── README.md
│
├── tools/
│   │
│   ├── validators.py
│   │
│   └── fitness/
│       ├── analyze.py
│       ├── recommend.py
│       ├── workout.py
│       └── plan.py
│
└── tests/
    ├── test_analyze.py
    ├── test_recommend.py
    ├── test_workout.py
    ├── test_complete_plan.py
    └── test_api.py
```

---

# Available Tools

## 1. Fitness Analysis

Tool:

```text
fitness.analyze
```

This tool analyzes a user's fitness profile and calculates:

- BMI
- BMI category
- BMR
- Maintenance calories
- Target calories
- Protein target
- Fat target
- Carbohydrate target

### Example Request

```json
{
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
```

---

## 2. Fitness Recommendations

Tool:

```text
fitness.recommend
```

This tool generates nutrition and training recommendations based on:

- Fitness goal
- Diet preference
- Daily calorie target

### Example Request

```json
{
    "tool": "fitness.recommend",
    "arguments": {
        "goal": "fat_loss",
        "diet_preference": "vegetarian",
        "daily_calories": 2045
    }
}
```

### Supported Goals

```text
fat_loss
maintenance
muscle_gain
```

### Supported Diet Preferences

```text
vegetarian
non_vegetarian
```

---

## 3. Workout Plan

Tool:

```text
fitness.workout_plan
```

This tool generates a workout plan based on:

- Fitness goal
- Experience level
- Training days per week
- Available equipment

### Example Request

```json
{
    "tool": "fitness.workout_plan",
    "arguments": {
        "goal": "fat_loss",
        "experience_level": "intermediate",
        "days_per_week": 5,
        "equipment": "gym"
    }
}
```

### Supported Experience Levels

```text
beginner
intermediate
advanced
```

### Supported Equipment

```text
gym
home
bodyweight
```

---

## 4. Complete Fitness Plan

Tool:

```text
fitness.complete_plan
```

This is the orchestration tool.

It combines:

```text
fitness.analyze
        +
fitness.recommend
        +
fitness.workout_plan
        =
Complete Fitness Plan
```

### Example Request

```json
{
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
```

---

# API Endpoint

FitFusion exposes a tool execution endpoint:

```text
POST /api/execute
```

Local URL:

```text
http://localhost:7071/api/execute
```

### Request Format

```json
{
    "tool": "fitness.analyze",
    "arguments": {}
}
```

The router uses the tool name to locate and execute the appropriate function from the tool registry.

---

# Validation

FitFusion validates:

- Required fields
- Invalid input objects
- String types
- Numeric types
- Positive numeric values
- Enum values
- Invalid goals
- Invalid diet preferences
- Invalid experience levels
- Invalid equipment
- Invalid training days

### Missing Field Example

```json
{
    "error": "Missing required field: name"
}
```

### Invalid Goal Example

```json
{
    "error": "Invalid goal",
    "allowed": [
        "fat_loss",
        "maintenance",
        "muscle_gain"
    ]
}
```

### Unknown Tool

Unknown tools return:

```text
HTTP 404
```

---

# Running Locally

## 1. Clone the Repository

```bash
git clone <your-repository-url>
cd fitfusion-api
```

## 2. Create a Virtual Environment

```powershell
python -m venv .venv
```

## 3. Activate the Virtual Environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

## 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

## 5. Start Azure Functions

```powershell
func start
```

The API will start locally at:

```text
http://localhost:7071
```

---

# Running Tests

Run the complete automated test suite:

```powershell
pytest -v
```

The test suite covers:

- Fitness analysis
- Fitness recommendations
- Workout plan generation
- Complete plan orchestration
- Required field validation
- Invalid input validation
- Invalid type validation
- Boundary testing
- Unknown tool handling
- API integration testing

Current test result:

```text
115 passed
```

---

# Example API Request

Using Python:

```python
import requests

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
    "http://localhost:7071/api/execute",
    json=payload
)

print(response.status_code)
print(response.json())
```

---

# Example Response

A successful request returns the executed tool and its result.

Example:

```json
{
    "tool": "fitness.complete_plan",
    "result": {
        "profile": {
            "age": 35,
            "gender": "male",
            "weight_kg": 72.5,
            "height_cm": 175,
            "activity_level": "moderate",
            "goal": "fat_loss"
        },
        "analysis": {
            "bmi": 23.67,
            "bmi_category": "normal",
            "bmr_calories": 1649,
            "maintenance_calories": 2556,
            "target_calories": 2045
        }
    }
}
```

---

# Design Principles

FitFusion follows a modular architecture:

```text
Validation
    |
    v
Router
    |
    v
Registry
    |
    v
Independent Tools
    |
    v
Orchestration
```

Each tool has a specific responsibility.

Shared validation logic is centralized in:

```text
tools/validators.py
```

This reduces duplicated code and makes the system easier to test and extend.

---

# Future Improvements

Potential next improvements:

- User authentication
- Database integration
- User profile storage
- Fitness progress tracking
- AI-powered meal generation
- Personalized exercise selection
- LLM integration
- Docker containerization
- Cloud deployment
- OpenAPI documentation
- CI/CD pipeline

---

# Author

Vijay Raju

AI / Cloud / Platform Engineering

---

# License

This project is currently intended for portfolio and learning purposes.