from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime
from typing import List
from .models import ConversationCreate, MessageCreate, ConversationResponse, Message
from .crud import (
    create_conversation,
    add_message,
    get_user_sessions,
    get_session,
)
from .db import conversations

app = FastAPI()

@app.post("/sessions/", response_model=ConversationResponse)
def start_conversation(user_id: str):
    # client generates or server generates UUID as session_id
    session_id = str(uuid4())
    doc = create_conversation(user_id, session_id)
    return ConversationResponse(
        user_id=user_id,
        session_id=session_id,
        created_at=doc["created_at"],
        messages=[],
    )

@app.post("/sessions/{user_id}/{session_id}/messages", response_model=Message)
def post_message(user_id: str, session_id: str, message: MessageCreate):
    conv = get_session(user_id, session_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    msg = add_message(user_id, session_id, message.sender, message.message)
    return msg

@app.get("/sessions/{user_id}/", response_model=List[ConversationResponse])
def list_sessions(user_id: str):
    convs = get_user_sessions(user_id)
    return [
        ConversationResponse(
            user_id=conv["user_id"],
            session_id=conv["session_id"],
            created_at=conv["created_at"],
            messages=[Message(**msg) for msg in conv.get("messages", [])],
        )
        for conv in convs
    ]

@app.get("/sessions/{user_id}/{session_id}", response_model=ConversationResponse)
def get_conversation(user_id: str, session_id: str):
    conv = get_session(user_id, session_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Session not found")
    return ConversationResponse(
        user_id=conv["user_id"],
        session_id=conv["session_id"],
        created_at=conv["created_at"],
        messages=[Message(**msg) for msg in conv.get("messages", [])],
    )
