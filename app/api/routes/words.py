from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime

from app.core.security import get_current_user
from app.db.session import get_db
from app.db.models.word import Word, DifficultyLevel
from app.db.models.practice_session import PracticeSession
from app.db.models.user import User
from app.db.schemas.word import WordCreate, WordRead, WordUpdate, WordStats

router = APIRouter(
    prefix="/words",
    tags=["Words"]
)


@router.post("", response_model=WordRead, status_code=status.HTTP_201_CREATED)
def create_word(
    word: WordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new word for the current user."""
    db_word = Word(
        **word.model_dump(),
        user_id=current_user.id
    )
    db.add(db_word)
    db.commit()
    db.refresh(db_word)
    return db_word


@router.get("", response_model=List[WordRead])
def list_words(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    difficulty: Optional[DifficultyLevel] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List words for the current user with filtering and pagination."""
    query = db.query(Word).filter(Word.user_id == current_user.id)

    if difficulty:
        query = query.filter(Word.difficulty == difficulty)
    if search:
        query = query.filter(Word.text.ilike(f"%{search}%"))

    return query.offset(skip).limit(limit).all()


@router.get("/{word_id}", response_model=WordRead)
def get_word(
    word_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific word by ID."""
    word = db.query(Word).filter(
        Word.id == word_id,
        Word.user_id == current_user.id
    ).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    return word


@router.put("/{word_id}", response_model=WordRead)
def update_word(
    word_id: int,
    word_update: WordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a word."""
    word = db.query(Word).filter(
        Word.id == word_id,
        Word.user_id == current_user.id
    ).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")

    for field, value in word_update.model_dump(exclude_unset=True).items():
        setattr(word, field, value)

    db.commit()
    db.refresh(word)
    return word


@router.delete("/{word_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_word(
    word_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a word."""
    word = db.query(Word).filter(
        Word.id == word_id,
        Word.user_id == current_user.id
    ).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")

    db.delete(word)
    db.commit()


@router.get("/{word_id}/stats", response_model=WordStats)
def get_word_stats(
    word_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get practice statistics for a word."""
    word = db.query(Word).filter(
        Word.id == word_id,
        Word.user_id == current_user.id
    ).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")

    stats = db.query(
        func.count(PracticeSession.id).label("total_practices"),
        func.sum(func.cast(PracticeSession.correct, Integer)
                 ).label("correct_answers"),
        func.max(PracticeSession.created_at).label("last_practiced")
    ).filter(
        PracticeSession.word_id == word_id,
        PracticeSession.user_id == current_user.id
    ).first()

    total = stats[0] or 0
    correct = stats[1] or 0
    success_rate = (correct / total * 100) if total > 0 else 0.0

    return WordStats(
        total_practices=total,
        correct_answers=correct,
        success_rate=success_rate,
        last_practiced=stats[2]
    )


@router.post("/{word_id}/practice")
def practice_word(
    word_id: int,
    correct: bool,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Record a practice session for a word."""
    word = db.query(Word).filter(
        Word.id == word_id,
        Word.user_id == current_user.id
    ).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")

    practice = PracticeSession(
        word_id=word_id,
        user_id=current_user.id,
        correct=correct
    )
    db.add(practice)
    db.commit()
    return {"status": "success"}
