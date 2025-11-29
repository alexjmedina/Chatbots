# app/services/whatsapp_service.py
# --------------------------------
# Conversión del servicio de WhatsApp. Usamos httpx para las peticiones HTTP.

import httpx
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)

class WhatsAppService:
    def __init__(self):
        self.base_url = f"{settings.BASE_URL}/{settings.API_VERSION}/{settings.BUSINESS_PHONE_ID}/messages"
        self.headers = {
            "Authorization": f"Bearer {settings.API_TOKEN}",
            "Content-Type": "application/json",
        }

    async def _send_request(self, data: dict):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.base_url, json=data, headers=self.headers)
                response.raise_for_status()
                logger.info(f"Message sent successfully: {response.json()}")
            except httpx.HTTPStatusError as e:
                logger.error(f"Error sending message to WhatsApp: {e.response.text}")
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")

    async def send_text_message(self, to: str, body: str):
        data = {
            "messaging_product": "whatsapp",
            "to": to,
            "text": {"body": body},
        }
        await self._send_request(data)

    async def mark_as_read(self, message_id: str):
        data = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id,
        }
        await self._send_request(data)

    # ... otros métodos como send_interactive_buttons, send_media_message, etc. se traducirían de manera similar
    # creando el diccionario `data` correspondiente y llamando a `_send_request`.

whatsapp_service = WhatsAppService()