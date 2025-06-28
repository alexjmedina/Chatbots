# app/api/webhook_routes.py
# -------------------------
# Equivalente a webhookController.js y webhookRoutes.js combinados.
# FastAPI fusiona estos conceptos.

from fastapi import APIRouter, Request, Response, HTTPException, status
from ..services.message_handler import message_handler
import logging

# Configuración del logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/webhook", tags=["Webhook"])
async def receive_webhook(request: Request):
    """
    Recibe los eventos de webhook de WhatsApp.
    """
    try:
        data = await request.json()
        logger.info(f"Incoming webhook message: {data}")

        message_data = data.get("entry", [{}])[0].get("changes", [{}])[0].get("value", {}).get("messages", [{}])[0]
        sender_info = data.get("entry", [{}])[0].get("changes", [{}])[0].get("value", {}).get("contacts", [{}])[0]

        if message_data:
            await message_handler.handle_incoming_message(message_data, sender_info)
        
        return Response(status_code=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/webhook", tags=["Webhook"])
async def verify_webhook(request: Request):
    """
    Verifica el webhook con Meta.
    """
    from ..core.config import settings
    
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == settings.WEBHOOK_VERIFY_TOKEN:
        logger.info("Webhook verified successfully!")
        return Response(content=challenge, status_code=status.HTTP_200_OK)
    else:
        logger.error("Webhook verification failed.")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Webhook verification failed: invalid token."
        )