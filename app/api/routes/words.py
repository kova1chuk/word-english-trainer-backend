from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db
from app.db.models.word import Word
from app.db.schemas.word import WordSchema

router = APIRouter(
    tags=["Words"],
)


@router.get(
    "",
    summary="List all words",
    description="Returns all words from the database.",
    response_model=List[WordSchema],
    status_code=status.HTTP_200_OK,
)
def list_words(db: Session = Depends(get_db)):
    """
    **List Words**

    Fetches all words from the database using SQLAlchemy ORM.
    """
    return db.query(Word).all()
