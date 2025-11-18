"""
Contact endpoints
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_active_user
from app.models import User, Contact
from app.schemas.contact import (
    ContactCreate,
    ContactUpdate,
    Contact as ContactSchema,
    ContactWithCompany,
    ContactList
)

router = APIRouter(prefix="/contacts", tags=["Contacts"])


@router.post("/", response_model=ContactWithCompany, status_code=status.HTTP_201_CREATED)
def create_contact(
    contact_data: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new contact"""
    new_contact = Contact(**contact_data.model_dump())

    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)

    return new_contact


@router.get("/", response_model=ContactList)
def list_contacts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    List contacts with pagination and optional search

    Args:
        page: Page number (starts at 1)
        page_size: Items per page (max 100)
        search: Optional search term for name/email
        db: Database session
        current_user: Current authenticated user

    Returns:
        Paginated list of contacts
    """
    query = db.query(Contact)

    # Apply search filter if provided
    if search:
        search_term = f"%{search}%"
        from sqlalchemy import or_, func
        query = query.filter(
            or_(
                func.lower(Contact.name).like(search_term.lower()),
                func.lower(Contact.surname).like(search_term.lower()),
                func.lower(Contact.email).like(search_term.lower()),
            )
        )

    # Get total count
    total = query.count()

    # Apply pagination
    offset = (page - 1) * page_size
    contacts = query.offset(offset).limit(page_size).all()

    return {
        "contacts": contacts,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{contact_id}", response_model=ContactWithCompany)
def get_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get contact by ID"""
    contact = db.query(Contact).filter(Contact.id == contact_id).first()

    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )

    return contact


@router.put("/{contact_id}", response_model=ContactWithCompany)
def update_contact(
    contact_id: int,
    contact_data: ContactUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update contact"""
    contact = db.query(Contact).filter(Contact.id == contact_id).first()

    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )

    # Update fields
    update_data = contact_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(contact, field, value)

    db.commit()
    db.refresh(contact)

    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete contact"""
    contact = db.query(Contact).filter(Contact.id == contact_id).first()

    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )

    db.delete(contact)
    db.commit()

    return None


@router.get("/{contact_id}/interactions")
def get_contact_interactions(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all interactions for a contact"""
    from app.models import Interaction

    contact = db.query(Contact).filter(Contact.id == contact_id).first()

    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )

    interactions = db.query(Interaction).filter(
        Interaction.contact_id == contact_id
    ).order_by(Interaction.interaction_date.desc()).all()

    return interactions
