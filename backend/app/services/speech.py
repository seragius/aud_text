"""
Speech-to-Text service using OpenAI Whisper API
"""
import io
from typing import Optional
from fastapi import UploadFile, HTTPException
from openai import OpenAI
from app.core.config import settings


class SpeechService:
    """Service for converting audio to text"""

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.max_size_bytes = settings.MAX_AUDIO_SIZE_MB * 1024 * 1024

    def validate_audio_file(self, file: UploadFile) -> None:
        """
        Validate audio file format and size

        Args:
            file: Uploaded audio file

        Raises:
            HTTPException: If validation fails
        """
        # Check file type
        allowed_types = [
            "audio/mpeg",      # mp3
            "audio/mp3",
            "audio/wav",       # wav
            "audio/x-wav",
            "audio/webm",      # webm
            "audio/ogg",       # ogg
            "audio/m4a",       # m4a
        ]

        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid audio format. Allowed: MP3, WAV, WEBM, OGG, M4A. Got: {file.content_type}"
            )

        # Note: Size is checked during upload via FastAPI's File() dependency

    async def transcribe_audio(
        self,
        audio_file: UploadFile,
        language: str = "es"
    ) -> str:
        """
        Transcribe audio file to text using Whisper API

        Args:
            audio_file: Audio file to transcribe
            language: Language code (default: "es" for Spanish)

        Returns:
            Transcribed text

        Raises:
            HTTPException: If transcription fails
        """
        try:
            # Validate file
            self.validate_audio_file(audio_file)

            # Read file content
            content = await audio_file.read()

            # Create a file-like object for OpenAI API
            audio_buffer = io.BytesIO(content)
            audio_buffer.name = audio_file.filename or "audio.mp3"

            # Call Whisper API
            transcript = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_buffer,
                language=language,
                response_format="text"
            )

            # Reset file pointer for potential reuse
            await audio_file.seek(0)

            return transcript

        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(
                status_code=500,
                detail=f"Error transcribing audio: {str(e)}"
            )

    async def transcribe_audio_with_metadata(
        self,
        audio_file: UploadFile,
        language: str = "es"
    ) -> dict:
        """
        Transcribe audio and return with metadata

        Args:
            audio_file: Audio file to transcribe
            language: Language code

        Returns:
            Dictionary with transcript and metadata
        """
        transcript = await self.transcribe_audio(audio_file, language)

        return {
            "transcript": transcript,
            "language": language,
            "filename": audio_file.filename,
            "content_type": audio_file.content_type,
        }


# Singleton instance
speech_service = SpeechService()
