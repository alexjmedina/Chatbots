# app/core/config.py
# ------------------
# Usamos Pydantic para un manejo de configuración robusto y tipado.
# Es superior a simplemente leer process.env.

import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    WEBHOOK_VERIFY_TOKEN: str
    API_TOKEN: str
    BUSINESS_PHONE_ID: str # Renombrado para mayor claridad
    API_VERSION: str = "v19.0"
    PORT: int = 8000
    BASE_URL: str = "https://graph.facebook.com"
    OPENAI_API_KEY: str
    GOOGLE_SHEETS_SPREADSHEET_ID: str

    class Config:
        # Esto permite que Pydantic lea las variables desde el archivo .env
        env_file = ".env"
        env_file_encoding = 'utf-8'

# Creamos una instancia única que será importada en el resto de la app
settings = Settings()