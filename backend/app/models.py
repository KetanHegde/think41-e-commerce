from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class Message(BaseModel):
    sender: str            # "user" or "ai"
    message: str
    timestamp: datetime

class ConversationCreate(BaseModel):
    user_id: str
    session_id: str
    messages: List[Message] = Field(default_factory=list)

class MessageCreate(BaseModel):
    sender: str
    message: str

class ConversationResponse(BaseModel):
    user_id: str
    session_id: str
    created_at: datetime
    messages: List[Message]
