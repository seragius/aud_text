"""
Pydantic schemas for Contact
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from .company import Company


class ContactBase(BaseModel):
    """Base contact schema"""
    company_id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=100)
    surname: Optional[str] = None
    position: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_mobile: Optional[str] = None
    phone_office: Optional[str] = None
    address: Optional[str] = None
    lead_type: Optional[str] = "lead"
    lead_status: Optional[str] = "new"
    lead_source: Optional[str] = None
    funnel_stage: Optional[str] = None


class ContactCreate(ContactBase):
    """Schema for creating a contact"""
    pass


class ContactUpdate(BaseModel):
    """Schema for updating a contact"""
    company_id: Optional[int] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    position: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_mobile: Optional[str] = None
    phone_office: Optional[str] = None
    address: Optional[str] = None
    lead_type: Optional[str] = None
    lead_status: Optional[str] = None
    lead_source: Optional[str] = None
    funnel_stage: Optional[str] = None


class Contact(ContactBase):
    """Public contact schema"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ContactWithCompany(Contact):
    """Contact schema with company details"""
    company: Optional[Company] = None

    class Config:
        from_attributes = True


class ContactList(BaseModel):
    """Schema for paginated contact list"""
    contacts: list[ContactWithCompany]
    total: int
    page: int
    page_size: int
