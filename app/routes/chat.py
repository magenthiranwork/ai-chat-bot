from fastapi import APIRouter

router = APIRouter()

# Fake database
shipments = {
    "TRK123": {
        "status": "In Transit",
        "location": "Chennai Hub"
    },
    "TRK456": {
        "status": "Delivered",
        "location": "Bangalore"
    }
}

@router.post("/chat")
def chat(payload: dict):
    message = payload.get("message", "").lower()

    if message.startswith("track"):
        parts = message.split()

        if len(parts) > 1:
            tracking_id = parts[1].upper()

            if tracking_id in shipments:
                shipment = shipments[tracking_id]
                return {
                    "reply": f"Tracking ID {tracking_id}\nStatus: {shipment['status']}\nLocation: {shipment['location']}"
                }
            else:
                return {
                    "reply": "Invalid tracking ID. Please check and try again."
                }

        return {
            "reply": "Please provide tracking ID. Example: track TRK123"
        }

    elif "price" in message:
        return {
            "reply": "Shipping starts at ₹50 per kg. Please share destination."
        }

    elif "pickup" in message:
        return {
            "reply": "Pickup scheduled. Please share your address."
        }

    else:
        return {
            "reply": "Welcome to Logistics Bot 🚚 How can I help you today?"
        }