import axios from "axios";
const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:8000";

export async function sendMessage({ user_id, message, conversation_id }) {
  const res = await axios.post(`${API_BASE}/api/chat`, {
    user_id,
    message,
    conversation_id,
  });
  return res.data;
}

export async function getConversations(user_id) {
  const res = await axios.get(`${API_BASE}/conversations/user/${user_id}`);
  return res.data;
}

export async function getConversationHistory(conversation_id) {
  const res = await axios.get(`${API_BASE}/conversations/${conversation_id}`);
  return res.data;
}
