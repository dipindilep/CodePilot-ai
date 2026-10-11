
import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:3b"


def generate_response(prompt: str, context: str = "") -> str:
    if context.strip():
        full_prompt = f"""
You are CodePilot AI, a software engineering assistant.

Use the retrieved repository code below to answer the user's question.
If the code does not contain enough information, say so instead of
inventing details. Clearly distinguish any general suggestions from
facts found in the repository.

Retrieved repository context:
{context}

User question:
{prompt}
"""
    else:
        full_prompt = prompt

    payload = {
        "model": MODEL_NAME,
        "prompt": full_prompt,
        "stream": False,
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120,
    )
    response.raise_for_status()

    data = response.json()
    return data["response"]
