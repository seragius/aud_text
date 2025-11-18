"""
NLP service for entity extraction using GPT-4
"""
import json
from typing import Dict, Any, Optional
from datetime import datetime
from dateutil import parser as date_parser
from openai import OpenAI
from fastapi import HTTPException
from app.core.config import settings


class NLPService:
    """Service for extracting entities from transcribed text"""

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def extract_entities(self, transcript: str) -> Dict[str, Any]:
        """
        Extract entities from transcribed text using GPT-4

        Entities extracted:
        - contact_name: Full name of the person mentioned
        - action_type: Type of interaction (meeting, call, email, etc.)
        - date: Date/time of the interaction
        - notes: Additional relevant information

        Args:
            transcript: Text from speech-to-text

        Returns:
            Dictionary with extracted entities
        """
        try:
            prompt = f"""Analiza el siguiente texto de una interacción comercial y extrae la información estructurada.

Texto: "{transcript}"

Debes extraer:
1. **contact_name**: Nombre completo de la persona mencionada (solo el nombre, sin empresa)
2. **action_type**: Tipo de acción (elige uno: "meeting", "call", "email", "note", "other")
3. **date**: Fecha y hora mencionada. Si es relativa (ej: "mañana", "próximo viernes"), calcula la fecha exacta asumiendo que hoy es {datetime.now().strftime('%Y-%m-%d')}. Formato ISO 8601.
4. **notes**: Resumen de los puntos clave mencionados

Si algún dato no está presente en el texto, usa null.

Responde SOLO con un objeto JSON válido con estas claves exactas:
{{
  "contact_name": "string o null",
  "action_type": "meeting|call|email|note|other",
  "date": "YYYY-MM-DDTHH:MM:SS o null",
  "notes": "string con resumen"
}}

No incluyas explicaciones adicionales, solo el JSON."""

            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un asistente experto en extracción de información de interacciones comerciales. Respondes únicamente con JSON válido."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.1,  # Low temperature for consistent extraction
            )

            # Parse JSON response
            extracted = json.loads(response.choices[0].message.content)

            # Validate and normalize
            return self._normalize_entities(extracted)

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error extracting entities: {str(e)}"
            )

    def _normalize_entities(self, entities: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize and validate extracted entities

        Args:
            entities: Raw extracted entities

        Returns:
            Normalized entities
        """
        normalized = {
            "contact_name": entities.get("contact_name"),
            "action_type": entities.get("action_type", "note"),
            "date": None,
            "notes": entities.get("notes", ""),
        }

        # Parse and validate date
        if entities.get("date"):
            try:
                # Try to parse the date string
                parsed_date = date_parser.parse(entities["date"])
                normalized["date"] = parsed_date
            except:
                # If parsing fails, use current time
                normalized["date"] = datetime.now()
        else:
            # If no date mentioned, use current time
            normalized["date"] = datetime.now()

        # Validate action type
        valid_actions = ["meeting", "call", "email", "note", "other"]
        if normalized["action_type"] not in valid_actions:
            normalized["action_type"] = "note"

        return normalized

    def parse_contact_name(self, full_name: Optional[str]) -> Dict[str, Optional[str]]:
        """
        Parse full name into name and surname

        Args:
            full_name: Full name string

        Returns:
            Dictionary with 'name' and 'surname' keys
        """
        if not full_name:
            return {"name": None, "surname": None}

        parts = full_name.strip().split(maxsplit=1)

        if len(parts) == 1:
            return {"name": parts[0], "surname": None}
        else:
            return {"name": parts[0], "surname": parts[1]}


# Singleton instance
nlp_service = NLPService()
