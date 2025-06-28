# app/services/message_handler.py
# -------------------------------
# La traducción más directa del cerebro del bot.
# ¡Nota el diccionario de estado en memoria, replicando el original!

from .whatsapp_service import whatsapp_service
# from .openai_service import openai_service  (asumimos que existe)
# from .google_sheets_service import append_to_sheet (asumimos que existe)
import logging

logger = logging.getLogger(__name__)

class MessageHandler:
    def __init__(self):
        # ADVERTENCIA: Este estado se mantiene en la memoria del servidor.
        # No es escalable y se perderá si el servidor se reinicia.
        # Se mantiene para una paridad 1:1 con la arquitectura original.
        self.appointment_state = {}
        self.assistand_state = {}

    async def handle_incoming_message(self, message: dict, sender_info: dict):
        message_type = message.get("type")
        from_number = message.get("from")
        message_id = message.get("id")

        if message_type == "text":
            body = message.get("text", {}).get("body", "").lower().strip()
            logger.info(f"Handling text message from {from_number}: '{body}'")
            
            # Aquí iría la misma lógica de if/elif/else del messageHandler.js
            if body in ["hola", "hello", "hi"]:
                name = sender_info.get("profile", {}).get("name", from_number)
                welcome_message = f"Hola {name}, Bienvenido a MEDPET en Python. ¿En qué puedo ayudarte hoy?"
                await whatsapp_service.send_text_message(from_number, welcome_message)
            else:
                # Ejemplo de respuesta eco
                echo_message = f"Echo desde Python: {body}"
                await whatsapp_service.send_text_message(from_number, echo_message)

            await whatsapp_service.mark_as_read(message_id)
        
        elif message_type == "interactive":
            # Lógica para botones interactivos
            pass
        
        # ... resto de la lógica

# Instancia única para ser usada por el controlador de webhook
message_handler = MessageHandler()