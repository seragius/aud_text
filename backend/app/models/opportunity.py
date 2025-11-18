"""
Opportunity model for sales pipeline
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric, Boolean, Date, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    contact_id = Column(Integer, ForeignKey("contacts.id", ondelete="CASCADE"), nullable=False)

    title = Column(String(255), nullable=False)
    value = Column(Numeric(15, 2))  # Potential deal value
    probability = Column(Integer, CheckConstraint('probability >= 0 AND probability <= 100'))  # 0-100%
    stage = Column(String(100))  # prospecting, qualification, proposal, negotiation, closing
    close_date = Column(Date, nullable=True)  # Expected closing date
    is_closed = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    contact = relationship("Contact", back_populates="opportunities")
