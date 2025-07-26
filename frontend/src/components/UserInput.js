import  { useState } from "react";

function UserInput({ onSend }) {
  const [val, setVal] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (val.trim() === "") return;
    onSend(val);
    setVal("");
  };

  return (
    <form onSubmit={handleSubmit} style={{display: "flex"}}>
      <input
        type="text"
        value={val}
        onChange={e => setVal(e.target.value)}
        placeholder="Type your message..."
        style={{flex: 1, padding: 12, borderRadius: 8, border: "1px solid #ccc"}}
      />
      <button type="submit" style={{marginLeft: 8, padding: "0 20px"}}>Send</button>
    </form>
  );
}

export default UserInput;
