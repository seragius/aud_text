"""
Interaction endpoints including voice processing
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_active_user
from app.models import User, Interaction
from app.schemas.interaction import (
    InteractionCreate,
    InteractionUpdate,
    Interaction as InteractionSchema,
    InteractionWithContact,
    InteractionList,
    VoiceProcessingResult
)
from app.services.speech import speech_service
from app.services.nlp import nlp_service
from app.services.crm import crm_service

router = APIRouter(prefix="/interactions", tags=["Interactions"])


@router.post("/voice", response_model=VoiceProcessingResult, status_code=status.HTTP_201_CREATED)
async def create_interaction_from_voice(
    audio: UploadFile = File(..., description="Audio file (MP3, WAV, WEBM, OGG)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create interaction from voice recording

    Process flow:
    1. Transcribe audio to text (Whisper)
    2. Extract entities from text (GPT-4)
    3. Match contact in database (fuzzy matching)
    4. Create interaction record

    Args:
        audio: Audio file to process
        db: Database session
        current_user: Current authenticated user

    Returns:
        Created interaction with extracted data
    """
    # Step 1: Transcribe audio
    transcript = await speech_service.transcribe_audio(audio)

    if not transcript or len(transcript.strip()) < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transcription too short or empty"
        )

    # Step 2: Extract entities from transcript
    entities = nlp_service.extract_entities(transcript)

    # Step 3: Find or create contact
    contact = None
    if entities.get("contact_name"):
        contact, created = crm_service.find_or_create_contact(
            db=db,
            full_name=entities["contact_name"],
            auto_create=False  # Don't auto-create, let user decide
        )

    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact '{entities.get('contact_name')}' not found in database. Please create the contact first or use manual entry."
        )

    # Step 4: Create interaction
    interaction = Interaction(
        user_id=current_user.id,
        contact_id=contact.id,
        type=entities.get("action_type", "note"),
        interaction_date=entities.get("date"),
        transcript=transcript,
        extracted_data=entities,
        notes=entities.get("notes", "")
    )

    db.add(interaction)
    db.commit()
    db.refresh(interaction)

    return {
        "interaction": interaction,
        "transcript": transcript,
        "extracted_entities": entities,
        "confidence": None  # Can be added later
    }


@router.post("/", response_model=InteractionWithContact, status_code=status.HTTP_201_CREATED)
def create_interaction(
    interaction_data: InteractionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create interaction manually"""
    new_interaction = Interaction(
        user_id=current_user.id,
        **interaction_data.model_dump()
    )

    db.add(new_interaction)
    db.commit()
    db.refresh(new_interaction)

    return new_interaction


@router.get("/", response_model=InteractionList)
def list_interactions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    contact_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    List interactions with pagination

    Args:
        page: Page number
        page_size: Items per page
        contact_id: Optional filter by contact
        db: Database session
        current_user: Current user

    Returns:
        Paginated list of interactions
    """
    query = db.query(Interaction).filter(Interaction.user_id == current_user.id)

    if contact_id:
        query = query.filter(Interaction.contact_id == contact_id)

    # Order by date descending
    query = query.order_by(Interaction.interaction_date.desc())

    # Get total
    total = query.count()

    # Paginate
    offset = (page - 1) * page_size
    interactions = query.offset(offset).limit(page_size).all()

    return {
        "interactions": interactions,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{interaction_id}", response_model=InteractionWithContact)
def get_interaction(
    interaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get interaction by ID"""
    interaction = db.query(Interaction).filter(
        Interaction.id == interaction_id,
        Interaction.user_id == current_user.id
    ).first()

    if not interaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interaction not found"
        )

    return interaction


@router.put("/{interaction_id}", response_model=InteractionWithContact)
def update_interaction(
    interaction_id: int,
    interaction_data: InteractionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update interaction"""
    interaction = db.query(Interaction).filter(
        Interaction.id == interaction_id,
        Interaction.user_id == current_user.id
    ).first()

    if not interaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interaction not found"
        )

    # Update fields
    update_data = interaction_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(interaction, field, value)

    db.commit()
    db.refresh(interaction)

    return interaction


@router.delete("/{interaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_interaction(
    interaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete interaction"""
    interaction = db.query(Interaction).filter(
        Interaction.id == interaction_id,
        Interaction.user_id == current_user.id
    ).first()

    if not interaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interaction not found"
        )

    db.delete(interaction)
    db.commit()

    return None
