from fastapi import FastAPI, HTTPException
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from .models import MessageCreate, ConversationResponse, Message, ChatRequest, ChatResponse
from .crud import (
    create_conversation,
    add_message_to_conversation,
    get_user_conversations,
    get_conversation,
    get_or_create_conversation,
    get_conversation_messages,
    find_order_for_llm,
    find_product_for_llm,
    find_user_for_llm,
)
from .llm_agent import run_llm
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] for stricter setup
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM_PROMPT = (
    "You are a helpful e-commerce assistant. "
    "If you are provided with order, user or product information as a system message, use it to give a clear, direct answer. "
    "If there is not enough information, ask a clarifying followup. "
    "When all required info is present, query the database and answer accordingly."
)

def ensure_str_id(id_):
    return str(id_) if not isinstance(id_, str) else id_

@app.post("/conversations/", response_model=ConversationResponse)
def start_conversation(user_id: str):
    conversation = create_conversation(user_id)
    return ConversationResponse(
        user_id=conversation["user_id"],
        conversation_id=ensure_str_id(conversation["_id"]),
        created_at=conversation["created_at"],
        messages=[],
    )

@app.post("/conversations/{conversation_id}/messages", response_model=Message)
def post_message(conversation_id: str, message: MessageCreate):
    conv = get_conversation(conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    msg = add_message_to_conversation(conversation_id, message.sender, message.message)
    return msg

@app.get("/conversations/user/{user_id}", response_model=List[ConversationResponse])
def list_conversations(user_id: str):
    convs = get_user_conversations(user_id)
    return [
        ConversationResponse(
            user_id=conv["user_id"],
            conversation_id=ensure_str_id(conv["_id"]),
            created_at=conv["created_at"],
            messages=[Message(**msg) for msg in conv.get("messages", [])],
        )
        for conv in convs
    ]

@app.get("/conversations/{conversation_id}", response_model=ConversationResponse)
def get_conversation_history(conversation_id: str):
    conv = get_conversation(conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return ConversationResponse(
        user_id=conv["user_id"],
        conversation_id=ensure_str_id(conv["_id"]),
        created_at=conv["created_at"],
        messages=[Message(**msg) for msg in conv.get("messages", [])],
    )

@app.post("/api/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    conv = get_or_create_conversation(request.user_id, request.conversation_id)
    conv_id = conv["_id"]
    add_message_to_conversation(conv_id, "user", request.message)
    messages = get_conversation_messages(conv_id)

    # Always produce format for LLM
    def convert_sender_to_role(sender: str) -> str:
        if sender == "user":
            return "user"
        elif sender == "ai":
            return "assistant"
        elif sender == "system":
            return "system"
        else:
            return "user"

    llm_messages = [
        {"role": convert_sender_to_role(msg.get("sender", "user")), "content": msg.get("message", "")}
        for msg in messages
    ]

    order_id = extract_order_id(llm_messages)
    product_id = extract_product_id(llm_messages)
    user_id_found = extract_user_id(llm_messages)

    db_info = None
    ai_response = None

    if order_id is not None:
        db_info = find_order_for_llm(order_id)
        if db_info:
            ai_response = run_llm(
                llm_messages + [{"role": "system", "content": db_info}],
                system_prompt=SYSTEM_PROMPT
            )
        else:
            ai_response = f"Sorry, I could not find an order with ID '{order_id}'. Please check your order ID."
    elif product_id is not None:
        db_info = find_product_for_llm(product_id)
        if db_info:
            ai_response = run_llm(
                llm_messages + [{"role": "system", "content": db_info}],
                system_prompt=SYSTEM_PROMPT
            )
        else:
            ai_response = f"Sorry, I could not find a product with ID '{product_id}'."
    elif user_id_found is not None:
        db_info = find_user_for_llm(user_id_found)
        if db_info:
            ai_response = run_llm(
                llm_messages + [{"role": "system", "content": db_info}],
                system_prompt=SYSTEM_PROMPT
            )
        else:
            ai_response = f"Sorry, I could not find a user with ID '{user_id_found}'."
    else:
        ai_response = run_llm(llm_messages, system_prompt=SYSTEM_PROMPT)

    add_message_to_conversation(conv_id, "ai", ai_response)
    messages = get_conversation_messages(conv_id)
    return ChatResponse(conversation_id=conv_id, messages=messages)

### Robust extraction helpers (return correct type)
def extract_order_id(messages) -> Optional[int]:
    for msg in reversed(messages):
        m = re.search(r"order id[:\-\s=]*([0-9]+)", msg.get("content", ""), re.IGNORECASE)
        if m:
            try:
                return int(m.group(1))
            except ValueError:
                continue
    return None

def extract_product_id(messages) -> Optional[int]:
    for msg in reversed(messages):
        m = re.search(r"product id[:\-\s=]*([0-9]+)", msg.get("content", ""), re.IGNORECASE)
        if m:
            try:
                return int(m.group(1))
            except ValueError:
                continue
        # secondary - handle SKU label if int
        m2 = re.search(r"sku[:\-\s=]*([0-9]+)", msg.get("content", ""), re.IGNORECASE)
        if m2:
            try:
                return int(m2.group(1))
            except ValueError:
                continue
    return None


def extract_user_id(messages) -> Optional[int]:
    for msg in reversed(messages):
        m = re.search(r"user id[:\-\s=]*([0-9]+)", msg.get("content", ""), re.IGNORECASE)
        if m:
            try:
                return int(m.group(1))
            except ValueError:
                continue
    return None
