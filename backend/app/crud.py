from .db import db, conversations
from datetime import datetime, timezone
from uuid import uuid4
from typing import Optional, Dict, Any, List

def create_conversation(user_id: str, conversation_id: Optional[str] = None):
    conversation_id = conversation_id or str(uuid4())
    doc = {
        "_id": conversation_id,
        "user_id": user_id,
        "created_at": datetime.now(timezone.utc),
        "messages": [],
    }
    conversations.insert_one(doc)
    return doc

def add_message_to_conversation(conversation_id: str, sender: str, message: str):
    msg = {
        "sender": sender,
        "message": message,
        "timestamp": datetime.now(timezone.utc)
    }
    conversations.update_one(
        {"_id": conversation_id},
        {"$push": {"messages": msg}}
    )
    return msg

def get_conversation(conversation_id: str):
    return conversations.find_one({"_id": conversation_id})

def get_user_conversations(user_id: str) -> List[dict]:
    return list(conversations.find({"user_id": user_id}).sort("created_at", -1))

def get_conversation_messages(conversation_id: str):
    conv = get_conversation(conversation_id)
    return conv.get("messages", []) if conv else []

def get_or_create_conversation(user_id: str, conversation_id: Optional[str] = None):
    if conversation_id:
        conv = get_conversation(conversation_id)
        if conv and conv["user_id"] == user_id:
            return conv
    return create_conversation(user_id, conversation_id)

### -- ECOMMERCE QUERIES -- ###
def get_order(order_id: int) -> Optional[Dict[str, Any]]:
    order = db['orders'].find_one({"order_id": order_id})
    if order:
        return {k: v for k, v in order.items() if k != "_id"}
    return None

def get_orders_by_user(user_id: int):
    return list(db['orders'].find({"user_id": user_id}))

def get_product(product_id: int):
    prod = db['products'].find_one({"id": product_id})
    if prod:
        return {k: v for k, v in prod.items() if k != "_id"}
    return None

def get_products_by_category(category: str):
    return list(db['products'].find({"category": category}))

def get_inventory_item(item_id: int):
    item = db['inventory_items'].find_one({"id": item_id})
    if item:
        return {k: v for k, v in item.items() if k != "_id"}
    return None

def get_inventory_by_product(product_id: int):
    return list(db['inventory_items'].find({"product_id": product_id}))

def get_user(user_id: int):
    user = db['users'].find_one({"id": user_id})
    if user:
        return {k: v for k, v in user.items() if k != "_id"}
    return None

def search_users_by_email(email: str):
    return list(db['users'].find({"email": email}))

def get_distribution_center(dc_id: int):
    dc = db['distribution_centers'].find_one({"id": dc_id})
    if dc:
        return {k: v for k, v in dc.items() if k != "_id"}
    return None

def get_distribution_centers():
    return list(db['distribution_centers'].find({}))

# LLM context helpers
def find_order_for_llm(order_id: int):
    order = get_order(order_id)
    if not order:
        return None
    return "Order Information:\n" + "\n".join([f"{k}: {v}" for k, v in order.items()])

def find_product_for_llm(product_id: int):
    prod = get_product(product_id)
    if not prod:
        return None
    return "Product Information:\n" + "\n".join([f"{k}: {v}" for k, v in prod.items()])

def find_user_for_llm(user_id: int):
    user = get_user(user_id)
    if not user:
        return None
    return "User Information:\n" + "\n".join([f"{k}: {v}" for k, v in user.items()])
