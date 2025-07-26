export default function Message({ sender, message, timestamp }) {
  const isUser = sender === "user";
  return (
    <div
      style={{
        display: "flex",
        flexDirection: isUser ? "row-reverse" : "row",
        margin: "10px 0",
        alignItems: "flex-end",
      }}
    >
      <div
        style={{
          background: isUser ? "#0084ff" : "#e6e6e6",
          color: isUser ? "#fff" : "#111",
          borderRadius: 16,
          padding: "8px 16px",
          maxWidth: 320,
          whiteSpace: "pre-wrap",
        }}
      >
        {message}
      </div>
      <div
        style={{
          alignSelf: "flex-end",
          fontSize: 12,
          color: "#888",
          margin: isUser ? "0 16px 0 0" : "0 0 0 16px",
        }}
      >
        {timestamp && new Date(timestamp).toLocaleTimeString()}
      </div>
    </div>
  );
}
