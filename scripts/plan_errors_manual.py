import requests
import json


url = "http://localhost:7071/api/tools/execute"


# Base valid arguments
base_arguments = {
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


# Test cases
test_cases = [
    {
        "name": "1. Missing name",
        "modify": lambda data: data.pop("name")
    },
    {
        "name": "2. Missing age",
        "modify": lambda data: data.pop("age")
    },
    {
        "name": "3. Invalid age type",
        "modify": lambda data: data.update({"age": "thirty five"})
    },
    {
        "name": "4. Invalid goal",
        "modify": lambda data: data.update(
            {"goal": "become_superhuman"}
        )
    },
    {
        "name": "5. Invalid diet preference",
        "modify": lambda data: data.update(
            {"diet_preference": "vegan"}
        )
    },
    {
        "name": "6. Invalid experience level",
        "modify": lambda data: data.update(
            {"experience_level": "expert"}
        )
    },
    {
        "name": "7. days_per_week = 0",
        "modify": lambda data: data.update(
            {"days_per_week": 0}
        )
    },
    {
        "name": "8. days_per_week = 8",
        "modify": lambda data: data.update(
            {"days_per_week": 8}
        )
    },
    {
        "name": "9. Invalid equipment",
        "modify": lambda data: data.update(
            {"equipment": "spaceship"}
        )
    },
    {
        "name": "10. Missing equipment",
        "modify": lambda data: data.pop("equipment")
    },
    {
        "name": "11. Weight is text instead of number",
        "modify": lambda data: data.update(
            {"weight": "seventy"}
        )
    },
    {
        "name": "12. Negative weight",
        "modify": lambda data: data.update(
            {"weight": -72.5}
        )
    }
]


print("\nStarting FitFusion Complete Plan Error Tests...\n")


for test in test_cases:

    # Create a fresh copy of valid data
    arguments = base_arguments.copy()

    # Apply invalid modification
    test["modify"](arguments)

    payload = {
        "tool": "fitness.complete_plan",
        "arguments": arguments
    }

    print("=" * 60)
    print("TEST:", test["name"])
    print("=" * 60)

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=30
        )

        print("Status:", response.status_code)

        try:
            result = response.json()
            print(
                json.dumps(
                    result,
                    indent=4
                )
            )
        except ValueError:
            print(response.text)

    except requests.exceptions.RequestException as e:
        print("Request failed:")
        print(e)

    print()


print("=" * 60)
print("FITFUSION ERROR TESTING COMPLETED")
print("=" * 60)