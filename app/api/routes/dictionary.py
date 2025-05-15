from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.security import get_current_user
from app.db.session import get_db
from app.db.models.dictionary import Dictionary
from app.db.models.user import User
from app.db.schemas.word import DictionaryCreate, DictionaryRead

router = APIRouter(
    prefix="/dictionary",
    tags=["Dictionary"]
)


@router.post("", response_model=DictionaryRead, status_code=status.HTTP_201_CREATED)
def create_dictionary_entry(
    entry: DictionaryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new dictionary entry."""
    existing = db.query(Dictionary).filter(
        Dictionary.text == entry.text,
        Dictionary.language == entry.language
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Entry already exists for '{entry.text}' in language '{entry.language}'"
        )

    db_entry = Dictionary(**entry.model_dump())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


@router.get("", response_model=List[DictionaryRead])
def list_dictionary_entries(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    language: Optional[str] = None,
    search: Optional[str] = None,
    difficulty: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List dictionary entries with filtering and pagination."""
    query = db.query(Dictionary)

    if language:
        query = query.filter(Dictionary.language == language)
    if search:
        query = query.filter(Dictionary.text.ilike(f"%{search}%"))
    if difficulty:
        query = query.filter(Dictionary.difficulty == difficulty)

    return query.offset(skip).limit(limit).all()


@router.get("/{entry_id}", response_model=DictionaryRead)
def get_dictionary_entry(
    entry_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific dictionary entry by ID."""
    entry = db.query(Dictionary).filter(Dictionary.id == entry_id).first()
    if not entry:
        raise HTTPException(
            status_code=404, detail="Dictionary entry not found")
    return entry


@router.put("/{entry_id}", response_model=DictionaryRead)
def update_dictionary_entry(
    entry_id: int,
    entry_update: DictionaryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a dictionary entry."""
    entry = db.query(Dictionary).filter(Dictionary.id == entry_id).first()
    if not entry:
        raise HTTPException(
            status_code=404, detail="Dictionary entry not found")

    # Check if the update would create a duplicate
    existing = db.query(Dictionary).filter(
        Dictionary.text == entry_update.text,
        Dictionary.language == entry_update.language,
        Dictionary.id != entry_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Entry already exists for '{entry_update.text}' in language '{entry_update.language}'"
        )

    for field, value in entry_update.model_dump().items():
        setattr(entry, field, value)

    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dictionary_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a dictionary entry."""
    entry = db.query(Dictionary).filter(Dictionary.id == entry_id).first()
    if not entry:
        raise HTTPException(
            status_code=404, detail="Dictionary entry not found")

    # Check if any words are using this dictionary entry
    if db.query(Word).filter(Word.dictionary_id == entry_id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete dictionary entry that is being used by users"
        )

    db.delete(entry)
    db.commit()
