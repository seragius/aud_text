"""
Pydantic schemas for Interaction
"""
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from .contact import ContactWithCompany


class InteractionBase(BaseModel):
    """Base interaction schema"""
    contact_id: int
    type: str = Field(..., min_length=1)
    interaction_date: datetime
    notes: Optional[str] = None


class InteractionCreate(InteractionBase):
    """Schema for creating an interaction manually"""
    pass


class InteractionFromVoice(BaseModel):
    """Schema for creating interaction from voice"""
    # This will be populated by the NLP service
    pass


class InteractionUpdate(BaseModel):
    """Schema for updating an interaction"""
    contact_id: Optional[int] = None
    type: Optional[str] = None
    interaction_date: Optional[datetime] = None
    notes: Optional[str] = None


class Interaction(InteractionBase):
    """Public interaction schema"""
    id: int
    user_id: int
    audio_url: Optional[str] = None
    transcript: Optional[str] = None
    extracted_data: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True


class InteractionWithContact(Interaction):
    """Interaction with contact details"""
    contact: Optional[ContactWithCompany] = None

    class Config:
        from_attributes = True


class InteractionList(BaseModel):
    """Schema for paginated interaction list"""
    interactions: list[InteractionWithContact]
    total: int
    page: int
    page_size: int


class VoiceProcessingResult(BaseModel):
    """Schema for voice processing result"""
    interaction: InteractionWithContact
    transcript: str
    extracted_entities: Dict[str, Any]
    confidence: Optional[float] = None
