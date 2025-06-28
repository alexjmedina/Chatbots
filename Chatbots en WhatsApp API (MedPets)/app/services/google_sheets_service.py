# app/services/google_sheets_service.py
# -------------------------------------
# Este servicio maneja la interacción con Google Sheets.

import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)

class GoogleSheetsService:
    def __init__(self):
        # Define los "scopes" o permisos que nuestra app necesita.
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        # La ruta al archivo de credenciales.
        self.KEY_FILE_LOCATION = os.path.join(os.getcwd(), 'credentials.json')
        self.spreadsheet_id = settings.GOOGLE_SHEETS_SPREADSHEET_ID
        
        # Cargamos las credenciales.
        try:
            self.credentials = Credentials.from_service_account_file(
                self.KEY_FILE_LOCATION, scopes=self.SCOPES)
        except FileNotFoundError:
            logger.error(f"FATAL: credentials.json not found at {self.KEY_FILE_LOCATION}. Please generate and place it in the root directory.")
            self.credentials = None

    def append_to_sheet(self, values: list, sheet_name: str = 'reservas') -> bool:
        """
        Añade una fila de datos a la hoja de cálculo especificada.
        `values` debe ser una lista de valores, ej: ["Juan Perez", "Cita", "2025-06-27"]
        """
        if not self.credentials:
            logger.error("Cannot append to sheet: Google credentials are not loaded.")
            return False
            
        try:
            # Construimos el cliente de la API
            service = build('sheets', 'v4', credentials=self.credentials)
            sheet = service.spreadsheets()

            # Preparamos el cuerpo de la petición
            body = {
                'values': [values]
            }

            logger.info(f"Appending data to sheet '{sheet_name}': {values}")
            
            # Hacemos la llamada a la API
            result = sheet.values().append(
                spreadsheetId=self.spreadsheet_id,
                range=f"{sheet_name}!A1", # Añadirá a la primera celda vacía de la hoja 'reservas'
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()
            
            logger.info(f"Data appended successfully: {result.get('updates').get('updatedCells')} cells updated.")
            return True

        except HttpError as err:
            logger.error(f"Google Sheets API error: {err}")
            return False
        except Exception as e:
            logger.error(f"An unexpected error occurred with Google Sheets: {e}")
            return False

# Instancia única del servicio
google_sheets_service = GoogleSheetsService()