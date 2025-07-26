import { useState } from "react";
import SidePanel from "./components/SidePanel";
import ChatWindow from "./components/ChatWindow";
import UserInput from "./components/UserInput";
import { sendMessage, getConversationHistory } from "./api";

// Make API functions available on window.api for SidePanel to use!
window.api = {
  getConversations: require("./api").getConversations,
  getConversationHistory,
};

function App() {
  const [userId] = useState("alice");
  const [conversationId, setConversationId] = useState(null);
  const [messages, setMessages] = useState([]);

  // For chat turn
  const handleSend = async (userMessage) => {
    try {
      const res = await sendMessage({
        user_id: userId,
        message: userMessage,
        conversation_id: conversationId,
      });
      setConversationId(res.conversation_id);
      setMessages(res.messages);
    } catch (err) {
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

  // When switching conversations
  const handleSelectSession = async (sessionId) => {
    setConversationId(sessionId);
    const hist = await window.api.getConversationHistory(sessionId);
    setMessages(hist.messages);
  };

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      <SidePanel
        userId={userId}
        onSelect={handleSelectSession}
        currentConversationId={conversationId}
      />
      <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>
        <div
          style={{
            flex: 1,
            padding: 16,
            overflowY: "auto",
            borderBottom: "1px solid #eee",
            background: "#f7f7f7",
          }}
        >
          <h2 style={{ textAlign: "center" }}>E-commerce Chatbot</h2>
          <ChatWindow messages={messages} />
        </div>
        <div style={{ padding: 16 }}>
          <UserInput onSend={handleSend} />
        </div>
      </div>
    </div>
  );
}

export default App;
