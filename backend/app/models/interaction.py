"""
Interaction model for tracking commercial interactions
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    contact_id = Column(Integer, ForeignKey("contacts.id", ondelete="CASCADE"), nullable=False)

    # Interaction details
    type = Column(String(50), nullable=False)  # meeting, call, email, note, etc.
    interaction_date = Column(DateTime(timezone=True), nullable=False, index=True)

    # Audio and transcription
    audio_url = Column(String(500), nullable=True)  # Path to stored audio file
    transcript = Column(Text, nullable=True)  # Full transcription from Whisper

    # Extracted data from NLP (stored as JSON for flexibility)
    extracted_data = Column(JSONB, nullable=True)

    # Additional notes
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="interactions")
    contact = relationship("Contact", back_populates="interactions")
