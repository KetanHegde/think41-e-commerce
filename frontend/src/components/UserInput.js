import { useState } from "react";

export default function UserInput({ onSend }) {
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
