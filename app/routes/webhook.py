from fastapi import APIRouter, Request
import requests
import os
from app.services.logistics import get_tracking_details

router = APIRouter()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")


# 🔹 Webhook Verification (Meta setup step)
@router.get("/webhook")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return int(challenge)

    return {"error": "Verification failed"}


# 🔹 Receive WhatsApp Messages
@router.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()

    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
        sender = data["entry"][0]["changes"][0]["value"]["messages"][0]["from"]

        if message.lower().startswith("track"):
            tracking_id = message.split(" ")[1]

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

        requests.post(url, headers=headers, json=payload)

    except Exception as e:
        print("Error:", e)

    return "ok"