import requests

payload = {
    "tool": "fitness.superhuman",
    "arguments": {}
}

response = requests.post(
    "http://localhost:7071/api/execute",
    json=payload
)

print("Status Code:", response.status_code)
print()
print("Response:")
print(response.text)