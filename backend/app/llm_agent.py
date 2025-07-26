import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def convert_sender_to_role(sender: str) -> str:
    if sender == "user":
        return "user"
    elif sender == "ai":
        return "assistant"
    elif sender == "system":
        return "system"
    else:
        # fallback/unknown sender
        return "user"

# Run LLM with conversation history for context and guidance
def run_llm(messages, system_prompt=None, model_name="llama-3.3-70b-versatile"):
    llm_messages = []
    if system_prompt:
        llm_messages.append({"role": "system", "content": system_prompt})
    for msg in messages:
        # Accept both {"sender":..., "message":...} and {"role":..., "content":...}
        if "sender" in msg and "message" in msg:
            llm_messages.append({
                "role": convert_sender_to_role(msg["sender"]),
                "content": msg["message"]
            })
        elif "role" in msg and "content" in msg:
            llm_messages.append(msg)
    completion = client.chat.completions.create(
        messages=llm_messages,
        model=model_name,
    )
    return completion.choices[0].message.content
