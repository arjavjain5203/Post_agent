from twilio.rest import Client
from backend.app.core.config import settings

class SmsService:
    def __init__(self):
        self.client = None
        self.from_number = settings.TWILIO_FROM_NUMBER
        if settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN:
            self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        else:
            print("Twilio credentials missing. SMS Service disabled.")

    def send_sms(self, to_number: str, body: str):
        if not self.client:
            print(f"MOCK SMS to {to_number}: {body}")
            return True
        
        try:
            # Ensure number has country code (rudimentary check)
            if not to_number.startswith('+'):
                to_number = f"+91{to_number}" # Default to India for this use case

            message = self.client.messages.create(
                body=body,
                from_=self.from_number,
                to=to_number
            )
            print(f"SMS sent: {message.sid}")
            return True
        except Exception as e:
            print(f"Failed to send SMS: {e}")
            return False

    def send_verification_code(self, to_number: str, code: str):
        body = f"Your verification code is: {code}. Do not share this with anyone."
        return self.send_sms(to_number, body)

    def send_maturity_alert(self, to_number: str, customer_name: str, amount: float):
        body = f"Alert: Investment for {customer_name} of Rs. {amount} has matured. Please follow up."
        return self.send_sms(to_number, body)

sms_service = SmsService()
