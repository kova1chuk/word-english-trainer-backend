from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.session import Base


class DifficultyLevel(str, enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    dictionary_id = Column(Integer, ForeignKey(
        "dictionary.id"), nullable=False)
    profile_id = Column(UUID(as_uuid=True), ForeignKey(
        "profiles.id"), nullable=False)
    personal_note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    # Relationships
    profile = relationship("Profile", back_populates="words")
    dictionary_entry = relationship("Dictionary")
    practice_sessions = relationship("PracticeSession", back_populates="word")
