from fastapi import FastAPI
from app.routes.chat import router as chat_router
from app.routes import webhook

app = FastAPI(title="Logistics Automation Bot")

app.include_router(webhook.router)

@app.get("/")
def root():
    return {"message": "Logistics Bot Backend Running"}