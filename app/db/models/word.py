from sqlalchemy import Column, Integer, String
from app.db.session import Base


class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, unique=True, index=True)
    meaning = Column(String)
