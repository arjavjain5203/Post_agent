
import requests
import pandas as pd
from io import BytesIO

BASE_URL = "http://127.0.0.1:8000/api/v1"
EMAIL = "test_verify@example.com"
MOBILE = "9988776655"
PASSWORD = "password123"

def verify():
    print("--- 1. Signup Agent ---")
    payload = {"name": "Test Agent", "mobile": MOBILE, "password": PASSWORD}
    r = requests.post(f"{BASE_URL}/auth/signup", json=payload)
    if r.status_code == 200:
        print("Signup: OK")
    else:
        print(f"Signup: {r.status_code} {r.text}")

    print("\n--- 2. Login ---")
    data = {"mobile": MOBILE, "password": PASSWORD}
    r = requests.post(f"{BASE_URL}/auth/login", json=data)
    token = r.json().get("access_token")
    if token:
        print("Login: OK")
    else:
        print(f"Login Failed: {r.text}")
        return

    headers = {"Authorization": f"Bearer {token}"}

    print("\n--- 3. Create Customer ---")
    cust_data = {"full_name": "John Doe", "mobile": "1234567890", "consent_flag": True}
    r = requests.post(f"{BASE_URL}/customers/", json=cust_data, headers=headers)
    if r.status_code == 200:
        cust = r.json()
        print(f"Customer Created: {cust['customer_id']} - {cust['full_name']}")
        cid = cust['customer_id']
    else:
        print(f"Customer Creation Failed: {r.text}")
        return

    print("\n--- 4. Create Investment ---")
    inv_data = {
        "customer_id": cid,
        "scheme_type": "NSC",
        "principal": 10000.0,
        "start_date": "2023-01-01",
        "maturity_date": "2028-01-01",
        "status": "ACTIVE"
    }
    r = requests.post(f"{BASE_URL}/investments/", json=inv_data, headers=headers)
    if r.status_code == 200:
        print("Investment Created: OK")
    else:
        print(f"Investment Creation Failed: {r.text}")

    print("\n--- 5. Bulk Upload (Excel) ---")
    # create dummy excel in memory
    df = pd.DataFrame([{
        "Name": "Alice Smith",
        "Mobile": "9876543210",
        "Scheme": "FD",
        "Principal": 50000,
        "StartDate": "2024-01-01",
        "MaturityDate": "2025-01-01"
    }])
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    
    files = {'file': ('test.xlsx', output, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
    r = requests.post(f"{BASE_URL}/upload/bulk", headers=headers, files=files)
    print(f"Upload Response: {r.status_code} {r.json()}")

if __name__ == "__main__":
    verify()
