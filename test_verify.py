
import requests

def test_verify():
    url = "http://127.0.0.1:8000/api/v1/auth/verify"
    payload = {
        "mobile": "9310082225",
        "otp": "282664"
    }
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_verify()
