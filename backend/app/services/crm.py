"""
CRM service for contact matching and business logic
"""
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from fuzzywuzzy import fuzz
from app.models import Contact, Company


class CRMService:
    """Service for CRM-specific business logic"""

    def __init__(self):
        self.fuzzy_threshold = 85  # Minimum similarity score for matching

    def find_contact_by_name(
        self,
        db: Session,
        full_name: str,
        use_fuzzy: bool = True
    ) -> Optional[Contact]:
        """
        Find a contact by name using exact or fuzzy matching

        Args:
            db: Database session
            full_name: Full name to search for
            use_fuzzy: Whether to use fuzzy matching

        Returns:
            Matched Contact or None
        """
        if not full_name:
            return None

        # Parse name
        parts = full_name.strip().split(maxsplit=1)
        name = parts[0]
        surname = parts[1] if len(parts) > 1 else None

        # Try exact match first
        query = db.query(Contact)

        if surname:
            # Search by name AND surname
            exact_match = query.filter(
                func.lower(Contact.name) == name.lower(),
                func.lower(Contact.surname) == surname.lower()
            ).first()

            if exact_match:
                return exact_match

        else:
            # Search by name only
            exact_match = query.filter(
                func.lower(Contact.name) == name.lower()
            ).first()

            if exact_match:
                return exact_match

        # If no exact match and fuzzy enabled, try fuzzy matching
        if use_fuzzy:
            return self._fuzzy_match_contact(db, full_name)

        return None

    def _fuzzy_match_contact(
        self,
        db: Session,
        full_name: str
    ) -> Optional[Contact]:
        """
        Find contact using fuzzy string matching

        Args:
            db: Database session
            full_name: Full name to match

        Returns:
            Best matching Contact or None
        """
        # Get all contacts
        contacts = db.query(Contact).all()

        best_match = None
        best_score = 0

        for contact in contacts:
            # Build full name for comparison
            contact_full_name = contact.full_name

            # Calculate similarity score
            score = fuzz.token_sort_ratio(
                full_name.lower(),
                contact_full_name.lower()
            )

            if score > best_score and score >= self.fuzzy_threshold:
                best_score = score
                best_match = contact

        return best_match

    def find_or_create_contact(
        self,
        db: Session,
        full_name: str,
        auto_create: bool = False
    ) -> Tuple[Optional[Contact], bool]:
        """
        Find existing contact or optionally create new one

        Args:
            db: Database session
            full_name: Full name to search
            auto_create: Whether to create if not found

        Returns:
            Tuple of (Contact, was_created)
        """
        # Try to find existing
        contact = self.find_contact_by_name(db, full_name)

        if contact:
            return contact, False

        # If not found and auto_create enabled
        if auto_create:
            parts = full_name.strip().split(maxsplit=1)
            name = parts[0]
            surname = parts[1] if len(parts) > 1 else None

            new_contact = Contact(
                name=name,
                surname=surname,
                lead_status="new",
                lead_source="voice_interaction"
            )

            db.add(new_contact)
            db.commit()
            db.refresh(new_contact)

            return new_contact, True

        return None, False

    def search_contacts(
        self,
        db: Session,
        query: str,
        limit: int = 20
    ) -> list[Contact]:
        """
        Search contacts by name, email, or company

        Args:
            db: Database session
            query: Search term
            limit: Maximum results

        Returns:
            List of matching contacts
        """
        search_term = f"%{query.lower()}%"

        contacts = db.query(Contact).filter(
            or_(
                func.lower(Contact.name).like(search_term),
                func.lower(Contact.surname).like(search_term),
                func.lower(Contact.email).like(search_term),
            )
        ).limit(limit).all()

        return contacts

    def get_contact_statistics(
        self,
        db: Session,
        contact_id: int
    ) -> dict:
        """
        Get statistics for a contact

        Args:
            db: Database session
            contact_id: Contact ID

        Returns:
            Dictionary with statistics
        """
        from app.models import Interaction, Opportunity

        contact = db.query(Contact).filter(Contact.id == contact_id).first()

        if not contact:
            return {}

        interaction_count = db.query(Interaction).filter(
            Interaction.contact_id == contact_id
        ).count()

        opportunity_count = db.query(Opportunity).filter(
            Opportunity.contact_id == contact_id
        ).count()

        return {
            "interaction_count": interaction_count,
            "opportunity_count": opportunity_count,
            "company_name": contact.company.name if contact.company else None,
        }


# Singleton instance
crm_service = CRMService()
