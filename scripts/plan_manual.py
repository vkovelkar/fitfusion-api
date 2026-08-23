import requests
import json


url = "http://localhost:7071/api/tools/execute"


payload = {
    "tool": "fitness.complete_plan",
    "arguments": {
        "name": "",
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


try:
    response = requests.post(
        url,
        json=payload,
        timeout=30
    )

    print("\nStatus:", response.status_code)
    print("\nResponse:")

    try:
        print(json.dumps(
            response.json(),
            indent=4
        ))
    except ValueError:
        print(response.text)

except requests.exceptions.RequestException as e:
    print("Request failed:")
    print(e)