from .db import conversations
from .models import ConversationCreate, MessageCreate
from datetime import datetime, timezone

# Create new session
def create_conversation(user_id: str, session_id: str):
    doc = {
        "user_id": user_id,
        "session_id": session_id,
        "created_at": datetime.now(timezone.utc),
        "messages": [],
    }
    conversations.insert_one(doc)
    return doc

# Append message to session
def add_message(user_id: str, session_id: str, sender: str, message: str):
    msg = {
        "sender": sender,
        "message": message,
        "timestamp": datetime.now(timezone.utc)
    }
    conversations.update_one(
        {"user_id": user_id, "session_id": session_id},
        {"$push": {"messages": msg}}
    )
    return msg

# Get all user sessions
def get_user_sessions(user_id: str):
    return list(conversations.find({"user_id": user_id}).sort("created_at", -1))

# Get a specific session
def get_session(user_id: str, session_id: str):
    return conversations.find_one({"user_id": user_id, "session_id": session_id})

# List all users (optional)
def get_users():
    return conversations.distinct("user_id")
