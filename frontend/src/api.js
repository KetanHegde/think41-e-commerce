import axios from "axios";

const API_BASE = "http://localhost:8000";  // Change if backend is different

export async function sendMessage({user_id, message, conversation_id}) {
  const res = await axios.post(`${API_BASE}/api/chat`, {
    user_id, message, conversation_id
  });
  return res.data;
}
