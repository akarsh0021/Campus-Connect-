import requests
import json

data = {
    "email": "ria.sharma@student.edu",
    "password": "student123"
}

headers = {"Content-Type": "application/json"}

print("Testing login...")
try:
    r = requests.post("http://127.0.0.1:8000/api/auth/login", json=data, headers=headers)
    print("Status:", r.status_code)
    print("Response:", r.text)
except Exception as e:
    print("Error:", e)
