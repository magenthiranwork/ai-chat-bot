from fastapi import APIRouter, Form
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse

router = APIRouter()

@router.post("/webhook")
async def whatsapp_webhook(Body: str = Form(...)):
    incoming_msg = Body.lower()

    response = MessagingResponse()

    if "price" in incoming_msg:
        reply = "Shipping starts at ₹50 per kg. Please share destination."

    elif incoming_msg.startswith("track"):
        parts = incoming_msg.split()
        if len(parts) > 1 and parts[1].upper() == "TRK123":
            reply = "Tracking ID TRK123\nStatus: In Transit\nLocation: Chennai Hub"
        else:
            reply = "Please provide valid tracking ID. Example: track TRK123"

    else:
        reply = "Welcome to Logistics Bot 🚚 How can I help you?"

    response.message(reply)

    return PlainTextResponse(str(response), media_type="application/xml")