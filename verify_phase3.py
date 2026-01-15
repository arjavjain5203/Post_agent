
import requests
import datetime
# We will use the existing customer/investment creation logic to seed data
# Then rely on the server logs to see if the "scheduler" picked it up.

BASE_URL = "http://127.0.0.1:8000/api/v1"
MOBILE = "9988776655"
PASSWORD = "password123"

def seed_data_and_verify():
    # 1. Login
    data = {"mobile": MOBILE, "password": PASSWORD}
    r = requests.post(f"{BASE_URL}/auth/login", json=data)
    token = r.json().get("access_token")
    if not token:
        print("Login Failed")
        return
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create Investment with maturity = TODAY + 10 days (F10 trigger)
    # To test logic, we need an investment that hits a trigger TODAY.
    # If today is X, and we want F10 (10 days before maturity), maturity must be X + 10.
    
    today = datetime.date.today()
    maturity_f10 = today + datetime.timedelta(days=10)
    
    # We need a customer first. Reuse existing if possible or create new.
    # Let's list customers first
    r = requests.get(f"{BASE_URL}/customers/", headers=headers)
    customers = r.json()
    if customers:
        cid = customers[0]['customer_id']
    else:
        # Create one
        r = requests.post(f"{BASE_URL}/customers/", json={"full_name": "Test Trigger", "mobile": "5555555555"}, headers=headers)
        cid = r.json()['customer_id']

    print(f"Seeding Investment for F10 Trigger (Maturity: {maturity_f10})")
    
    inv_data = {
        "customer_id": cid,
        "scheme_type": "KVP",
        "principal": 25000.0,
        "start_date": str(today - datetime.timedelta(days=365)), # Started a year ago
        "maturity_date": str(maturity_f10),
        "status": "ACTIVE"
    }
    
    r = requests.post(f"{BASE_URL}/investments/", json=inv_data, headers=headers)
    print(f"Seed Response: {r.status_code}")
    
    print("\n--- Verification Instructions ---")
    print("1. The server startup triggered 'check_daily_followups'.")
    print("2. Check the server console/logs.")
    print("3. You should see: '[MOCK WHATSAPP] To: ... Template: investment_maturity_alert ...'")
    print("4. This confirms the engine found the F10 investment and sent the alert.")

if __name__ == "__main__":
    seed_data_and_verify()
