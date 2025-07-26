import MessageList from "./MessageList";
import UserInput from "./UserInput";

function ChatWindow({ messages, onSend }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", height: 500 }}>
      <div
        style={{
          flex: 1,
          padding: 16,
          overflowY: "auto",
          borderBottom: "1px solid #ccc",
        }}
      >
        <MessageList messages={messages} />
      </div>
      <div style={{ padding: 16 }}>
        <UserInput onSend={onSend} />
      </div>
    </div>
  );
}

export default ChatWindow;
