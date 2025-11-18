"""
Pydantic schemas for Company
"""
from datetime import datetime
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field, HttpUrl


class CompanyBase(BaseModel):
    """Base company schema"""
    name: str = Field(..., min_length=1, max_length=255)
    sector: Optional[str] = None
    size: Optional[str] = None
    employees: Optional[int] = None
    revenue: Optional[Decimal] = None
    website: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None


class CompanyCreate(CompanyBase):
    """Schema for creating a company"""
    pass


class CompanyUpdate(BaseModel):
    """Schema for updating a company"""
    name: Optional[str] = None
    sector: Optional[str] = None
    size: Optional[str] = None
    employees: Optional[int] = None
    revenue: Optional[Decimal] = None
    website: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None


class Company(CompanyBase):
    """Public company schema"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CompanyWithContacts(Company):
    """Company schema with contact count"""
    contact_count: int = 0

    class Config:
        from_attributes = True
