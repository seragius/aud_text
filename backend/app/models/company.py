"""
Company model for B2B contacts
"""
from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    sector = Column(String(100))
    size = Column(String(50))  # Small, Medium, Large, Enterprise
    employees = Column(Integer)
    revenue = Column(Numeric(15, 2))  # Annual revenue
    website = Column(String(255))
    country = Column(String(100))
    city = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    contacts = relationship("Contact", back_populates="company", cascade="all, delete-orphan")
