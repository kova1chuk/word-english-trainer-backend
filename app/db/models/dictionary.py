from sqlalchemy import Column, Integer, String, Text, Enum
from app.db.session import Base
from app.db.models.word import DifficultyLevel


class Dictionary(Base):
    __tablename__ = "dictionary"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, unique=True, index=True)
    meaning = Column(Text)
    example = Column(Text, nullable=True)
    pronunciation = Column(String, nullable=True)
    difficulty = Column(Enum(DifficultyLevel), default=DifficultyLevel.MEDIUM)
    language = Column(String, index=True)  # e.g., "en", "es", "fr"

    def __repr__(self):
        return f"<Dictionary(text={self.text}, language={self.language})>"
