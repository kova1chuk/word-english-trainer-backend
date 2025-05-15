from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid


class ProfileBase(BaseModel):
    name: Optional[str] = Field(None, description="User's display name")
    native_language: Optional[str] = Field(
        None, description="User's native language code (e.g., 'en')")
    target_language: Optional[str] = Field(
        None, description="Language being learned (e.g., 'es')")


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    pass


class ProfileRead(ProfileBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
