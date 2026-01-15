import httpx
from typing import List, Optional
from backend.app.core.config import settings

async def send_whatsapp_template(to_mobile: str, template_name: str, params: List[str]):
    """
    Sends a WhatsApp template message.
    If credentials are not set, falls back to printing to console (Mock Mode).
    """
    if not settings.WHATSAPP_TOKEN or not settings.WHATSAPP_PHONE_ID:
        # Mock Mode
        print(f"--- [MOCK WHATSAPP] To: {to_mobile} | Template: {template_name} | Params: {params} ---")
        return True

    url = f"https://graph.facebook.com/v17.0/{settings.WHATSAPP_PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Construct payload for template (simplified for MVP)
    # Assuming params are body text parameters
    components = []
    if params:
        components.append({
            "type": "body",
            "parameters": [{"type": "text", "text": p} for p in params]
        })

    payload = {
        "messaging_product": "whatsapp",
        "to": to_mobile,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": "en_US"},
            "components": components
        }
    }

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            return True
        except httpx.HTTPError as e:
            print(f"WhatsApp API Error: {e}")
            if hasattr(e, 'response'):
                print(e.response.text)
            return False
