from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.db.models.word import DifficultyLevel
import uuid


class DictionaryBase(BaseModel):
    text: str = Field(..., description="The word or phrase to learn")
    meaning: str = Field(...,
                         description="The meaning or translation of the word")
    example: Optional[str] = Field(
        None, description="An example sentence using the word")
    pronunciation: Optional[str] = Field(
        None, description="Pronunciation guide or IPA notation")
    difficulty: DifficultyLevel = Field(
        default=DifficultyLevel.MEDIUM, description="Difficulty level of the word")
    language: str = Field(...,
                          description="Language of the word (e.g., 'en', 'es')")


class DictionaryCreate(DictionaryBase):
    pass


class DictionaryRead(DictionaryBase):
    id: int

    class Config:
        from_attributes = True


class WordBase(BaseModel):
    dictionary_id: int = Field(...,
                               description="Reference to the dictionary entry")
    personal_note: Optional[str] = Field(
        None, description="User's personal note about the word")


class WordCreate(WordBase):
    pass


class WordUpdate(BaseModel):
    personal_note: Optional[str] = None


class WordRead(WordBase):
    id: int
    created_at: datetime
    updated_at: datetime
    profile_id: uuid.UUID
    dictionary_entry: DictionaryRead

    class Config:
        from_attributes = True


class WordStats(BaseModel):
    total_practices: int
    correct_answers: int
    success_rate: float
    last_practiced: Optional[datetime]
