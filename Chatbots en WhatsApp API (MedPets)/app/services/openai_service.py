# app/services/openai_service.py
# -------------------------------
# Este servicio se encarga de toda la comunicación con la API de OpenAI.

from openai import AsyncOpenAI
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        # Es una buena práctica inicializar el cliente una sola vez.
        # El cliente es asíncrono para no bloquear la aplicación.
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-4o" # Modelo recomendado por su balance de velocidad y potencia

    async def get_vet_response(self, user_query: str) -> str:
        """
        Genera una respuesta de IA para una consulta veterinaria.
        """
        # Este es el "system prompt" que define la personalidad y el rol del bot.
        system_prompt = (
            'Eres parte de un servicio de asistencia online y debes de comportarte como un '
            'veterinario de un comercio llamado "MedPet". Resuelve las preguntas lo más simple '
            'posible, con una explicación posible. Si es una emergencia o debe de llamarnos '
            '(MedPet). Debes de responder en texto simple como si fuera un mensaje de un '
            'bot conversacional, no saludes, no generes conversación, solo respondes con '
            'la pregunta del usuario.'
        )
        
        try:
            logger.info(f"Sending query to OpenAI: {user_query}")
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ],
                temperature=0.7, # Un poco de creatividad pero sin alucinar.
                max_tokens=150   # Limita la longitud de la respuesta.
            )
            ai_response = response.choices[0].message.content.strip()
            logger.info(f"Received response from OpenAI: {ai_response}")
            return ai_response
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            return "Lo siento, estoy teniendo problemas para conectarme con mi cerebro de IA en este momento. Por favor, intenta de nuevo más tarde."

# Creamos una instancia única para ser importada en otros módulos.
openai_service = OpenAIService()