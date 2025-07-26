import { useState, useRef, useEffect } from "react";
import ChatWindow from "./components/ChatWindow";
import { sendMessage } from "./api";

function App() {
  const [userId] = useState("alice");
  const [conversationId, setConversationId] = useState(null);
  const [messages, setMessages] = useState([]);
  const messagesEndRef = useRef(null);

  // Scrolls to bottom automatically on new message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Handles sending user message and receiving new messages from backend
  const handleSend = async (userMessage) => {
    if (!userMessage || !userMessage.trim()) return;
    try {
      const res = await sendMessage({
        user_id: userId,
        message: userMessage,
        conversation_id: conversationId,
      });
      setConversationId(res.conversation_id);
      setMessages(res.messages);
    } catch (err) {
      // Show network or backend error
      setMessages((msgs) => [
        ...msgs,
        {
          sender: "ai",
          message: "Could not reach chatbot backend. Try again.",
          timestamp: new Date().toISOString(),
        },
      ]);
    }
  };

  return (
    <div
      style={{
        maxWidth: 600,
        margin: "40px auto",
        border: "1px solid #ccc",
        borderRadius: 12,
        background: "#f7f7f7",
        boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
      }}
    >
      <h2 style={{ textAlign: "center", marginBottom: 0, padding: 16 }}>
        E-commerce Chatbot
      </h2>
      <div
        style={{
          padding: 16,
          height: 500,
          overflowY: "auto",
          borderBottom: "1px solid #eee",
        }}
      >
        <ChatWindow messages={messages} />
        <div ref={messagesEndRef} /> {/* The scroll anchor */}
      </div>
      <div style={{ padding: 16 }}>
        <UserInput onSend={handleSend} />
      </div>
    </div>
  );
}

function UserInput({ onSend }) {
  const [val, setVal] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (val.trim() !== "") {
      onSend(val.trim());
      setVal("");
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: "flex" }}>
      <input
        type="text"
        value={val}
        onChange={(e) => setVal(e.target.value)}
        placeholder="Type your message…"
        style={{
          flex: 1,
          padding: 12,
          borderRadius: 8,
          border: "1px solid #ccc",
        }}
      />
      <button
        type="submit"
        style={{
          marginLeft: 8,
          padding: "0 20px",
          borderRadius: 8,
          border: "none",
          background: "#0084ff",
          color: "#fff",
        }}
      >
        Send
      </button>
    </form>
  );
}

export default App;
