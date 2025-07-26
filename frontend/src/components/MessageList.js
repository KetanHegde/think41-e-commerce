import Message from "./Message";

function MessageList({ messages }) {
  return (
    <div>
      {messages.map((msg, idx) => (
        <Message key={idx} {...msg} />
      ))}
    </div>
  );
}

export default MessageList;
