import React, { useEffect, useState } from "react";

function SidePanel({ userId, onSelect, currentConversationId }) {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchSessions() {
      setLoading(true);
      try {
        const list = await window.api.getConversations(userId);
        setSessions(list);
      } catch (e) {
        setSessions([]);
      }
      setLoading(false);
    }
    if (userId) fetchSessions();
  }, [userId]);

  return (
    <div
      style={{
        width: 220,
        borderRight: "1px solid #eee",
        height: "100vh",
        overflowY: "auto",
        background: "#f8f8f8",
      }}
    >
      <div
        style={{
          padding: 12,
          fontWeight: "bold",
          borderBottom: "1px solid #eee",
        }}
      >
        Your Chats
      </div>
      {loading && <div style={{ padding: 16 }}>Loading…</div>}
      {!loading && sessions.length === 0 && (
        <div style={{ padding: 16, color: "#888" }}>No previous sessions</div>
      )}
      <ul style={{ listStyle: "none", margin: 0, padding: 0 }}>
        {sessions.map((sess) => (
          <li
            key={sess.conversation_id}
            style={{
              padding: 12,
              cursor: "pointer",
              background:
                currentConversationId === sess.conversation_id
                  ? "#ddeeff"
                  : "none",
              borderBottom: "1px solid #eee",
            }}
            onClick={() => onSelect(sess.conversation_id)}
            title={new Date(sess.created_at).toLocaleString()}
          >
            <div>
              <b>Started:</b> {new Date(sess.created_at).toLocaleDateString()}
            </div>
            <div style={{ fontSize: 12, color: "#666" }}>
              {sess.messages.length} messages
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default SidePanel;
