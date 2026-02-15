from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse
import requests
import os
from app.services.logistics import get_tracking_details

router = APIRouter()

# 🔥 Hardcode temporarily to avoid env mismatch
VERIFY_TOKEN = "logistics_secure_2026"

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")


@router.get("/webhook")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    print("Mode:", mode)
    print("Token from request:", token)
    print("Expected token:", VERIFY_TOKEN)

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(content=challenge, status_code=200)

    # return OK for normal checks instead of 403
    return PlainTextResponse(content="OK", status_code=200)


# 🔹 Receive WhatsApp Messages
@router.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()
    print("---- INCOMING POST ----")
    print(data)

    try:
        entry = data.get("entry", [])
        if not entry:
            return PlainTextResponse(content="No entry field", status_code=200)

        changes = entry[0].get("changes", [])
        if not changes:
            return PlainTextResponse(content="No changes field", status_code=200)

        value = changes[0].get("value", {})
        messages = value.get("messages")

        # If no actual message (like delivery/read events)
        if not messages:
            return PlainTextResponse(content="No messages field", status_code=200)

        message_data = messages[0]
        message = message_data.get("text", {}).get("body", "")
        sender = message_data.get("from")

        if not message or not sender:
            return PlainTextResponse(content="Invalid message format", status_code=200)

        print("Sender:", sender)
        print("Message:", message)

        if message.lower().startswith("track"):
            parts = message.split(" ")

            if len(parts) < 2:
                reply_text = "Please send: track <TrackingID>"
            else:
                tracking_id = parts[1]
                tracking_data = get_tracking_details(tracking_id)

                reply_text = f"""
Tracking ID: {tracking_data['tracking_id']}
Container: {tracking_data['container_number']}
Status: {tracking_data['status']}
Last Location: {tracking_data['last_location']}
ETA: {tracking_data['eta']}
History:
{tracking_data['history']}
"""
        else:
            reply_text = "Please send: track <TrackingID>"

        # 🔹 Send reply back to WhatsApp
        url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

        payload = {
            "messaging_product": "whatsapp",
            "to": sender,
            "text": {"body": reply_text.strip()}
        }

        response = requests.post(url, headers=headers, json=payload)

        print("WhatsApp API Status:", response.status_code)
        print("WhatsApp API Response:", response.text)

    except Exception as e:
        print("🔥 Error occurred:", str(e))

    return PlainTextResponse(content="ok", status_code=200)