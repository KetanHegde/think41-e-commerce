import Message from "./Message";

export default function MessageList({ messages }) {
  return (
    <div>
      {messages.map((msg, idx) => (
        <Message key={idx} {...msg} />
      ))}
    </div>
  );
}
