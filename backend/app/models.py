from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class Message(BaseModel):
    sender: str         # "user" or "ai"
    message: str
    timestamp: datetime

class MessageCreate(BaseModel):
    sender: str
    message: str

class ConversationResponse(BaseModel):
    user_id: str
    conversation_id: str
    created_at: datetime
    messages: List[Message]

class ChatRequest(BaseModel):
    user_id: str
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    conversation_id: str
    messages: List[dict]
