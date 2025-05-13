from pydantic import BaseModel


class WordSchema(BaseModel):
    id: int
    text: str
    meaning: str

    class Config:
        orm_mode = True
