"""
Pydantic schemas for Opportunity
"""
from datetime import datetime, date
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field


class OpportunityBase(BaseModel):
    """Base opportunity schema"""
    contact_id: int
    title: str = Field(..., min_length=1, max_length=255)
    value: Optional[Decimal] = None
    probability: Optional[int] = Field(None, ge=0, le=100)
    stage: Optional[str] = None
    close_date: Optional[date] = None


class OpportunityCreate(OpportunityBase):
    """Schema for creating an opportunity"""
    pass


class OpportunityUpdate(BaseModel):
    """Schema for updating an opportunity"""
    contact_id: Optional[int] = None
    title: Optional[str] = None
    value: Optional[Decimal] = None
    probability: Optional[int] = Field(None, ge=0, le=100)
    stage: Optional[str] = None
    close_date: Optional[date] = None
    is_closed: Optional[bool] = None


class Opportunity(OpportunityBase):
    """Public opportunity schema"""
    id: int
    is_closed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
