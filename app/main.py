from fastapi import FastAPI
from app.routes import webhook
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="Logistics Automation Bot")

# Include webhook router
app.include_router(webhook.router)

@app.get("/")
def root():
    return {"message": "Logistics Bot Backend Running"}