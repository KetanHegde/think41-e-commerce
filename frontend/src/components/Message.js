import React from "react";

function Message({ sender, message, timestamp }) {
  const isUser = sender === "user";
  return (
    <div style={{
      display: "flex",
      flexDirection: isUser ? "row-reverse" : "row",
      margin: "8px 0"
    }}>
      <div style={{
        background: isUser ? "#0084ff" : "#e6e6e6",
        color: isUser ? "#fff" : "#111",
        borderRadius: 16,
        padding: "8px 16px",
        maxWidth: 320,
        whiteSpace: "pre-wrap"
      }}>
        <b>{isUser ? "You" : "Bot"}: </b>{message}
      </div>
      <div style={{alignSelf: "flex-end", fontSize: 12, color: "#888", margin: isUser ? "0 12px 0 0" : "0 0 0 12px"}}>
        {timestamp && (new Date(timestamp)).toLocaleTimeString()}
      </div>
    </div>
  );
}

export default Message;
