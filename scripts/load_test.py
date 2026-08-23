import concurrent.futures
import requests
import time

URL = "http://localhost:8080/api/tools/execute"

PAYLOAD = {
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

TOTAL_REQUESTS = 5000
CONCURRENT_USERS = 100


def send_request(request_number):
    try:
        response = requests.post(
            URL,
            json=PAYLOAD,
            timeout=30
        )

        return response.status_code

    except Exception as error:
        return f"ERROR: {error}"


def main():

    print("=" * 60)
    print("FitFusion API Load Test")
    print("=" * 60)

    print(f"Target URL: {URL}")
    print(f"Total Requests: {TOTAL_REQUESTS}")
    print(f"Concurrent Users: {CONCURRENT_USERS}")
    print()

    start_time = time.time()

    results = []

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=CONCURRENT_USERS
    ) as executor:

        futures = [
            executor.submit(send_request, i)
            for i in range(TOTAL_REQUESTS)
        ]

        for future in concurrent.futures.as_completed(futures):

            result = future.result()

            results.append(result)

    end_time = time.time()

    duration = end_time - start_time

    successful = results.count(200)

    failed = len(results) - successful

    print()
    print("=" * 60)
    print("LOAD TEST RESULTS")
    print("=" * 60)

    print(f"Total Requests : {len(results)}")
    print(f"Successful     : {successful}")
    print(f"Failed         : {failed}")
    print(f"Duration       : {duration:.2f} seconds")

    if duration > 0:
        print(
            f"Requests/sec   : "
            f"{len(results) / duration:.2f}"
        )


if __name__ == "__main__":
    main()