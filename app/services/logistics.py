import requests

def get_tracking_details(tracking_id: str):

    # 🔹 Example External API call
    # response = requests.get(f"https://external-logistics.com/api/{tracking_id}")
    # data = response.json()

    # 🔹 Mocked response for now
    return {
        "tracking_id": tracking_id,
        "container_number": "MSKU1234567",
        "status": "In Transit",
        "last_location": "Chennai Port",
        "eta": "2026-02-15",
        "history": """
- 01 Feb: Departed Singapore
- 03 Feb: Arrived Colombo
- 05 Feb: Reached Chennai
"""
    }