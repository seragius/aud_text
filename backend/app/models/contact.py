"""
Contact model for CRM
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="SET NULL"), nullable=True)

    # Personal info
    name = Column(String(100), nullable=False, index=True)
    surname = Column(String(100), index=True)
    position = Column(String(100))  # Job title

    # Contact info
    email = Column(String(255), index=True)
    phone_mobile = Column(String(50))
    phone_office = Column(String(50))
    address = Column(Text)

    # Lead management
    lead_type = Column(String(50), default="lead")  # lead, prospect, client, partner
    lead_status = Column(String(50), default="new")  # new, contacted, qualified, unqualified
    lead_source = Column(String(100))  # web, email, event, referral, social_media
    funnel_stage = Column(String(100))  # prospection, negotiation, closing

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    company = relationship("Company", back_populates="contacts")
    interactions = relationship("Interaction", back_populates="contact", cascade="all, delete-orphan")
    opportunities = relationship("Opportunity", back_populates="contact", cascade="all, delete-orphan")

    @property
    def full_name(self) -> str:
        """Get full name"""
        if self.surname:
            return f"{self.name} {self.surname}"
        return self.name
