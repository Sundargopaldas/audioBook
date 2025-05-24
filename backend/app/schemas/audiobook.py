from pydantic import BaseModel
from typing import Optional

class AudiobookBase(BaseModel):
    title: str
    status: str
    progress: float = 0
    current_step: int = 0
    error: Optional[str] = None
    audio_url: Optional[str] = None

class AudiobookCreate(AudiobookBase):
    user_id: int

class AudiobookUpdate(AudiobookBase):
    pass

class AudiobookResponse(AudiobookBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class AudiobookStatus(BaseModel):
    status: str
    progress: float
    current_step: int
    error: Optional[str] = None 