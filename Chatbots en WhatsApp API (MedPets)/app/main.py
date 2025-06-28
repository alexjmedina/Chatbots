# app/main.py
# -----------
# Punto de entrada de FastAPI. Simple y limpio.

from fastapi import FastAPI
from .api import webhook_routes

app = FastAPI(
    title="WhatsApp Chatbot API",
    description="Backend para un chatbot de WhatsApp en Python",
    version="1.0.0"
)

# Incluimos las rutas definidas en otro archivo
app.include_router(webhook_routes.router)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Nothing to see here. Checkout /docs for API documentation."}