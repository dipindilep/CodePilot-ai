import requests


OLLAMA_URL = "http://localhost:11434/api/generate"


def generate_response(prompt: str) -> str:

    payload = {
        "model": "qwen2.5-coder:3b",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload
    )

    data = response.json()

    return data["response"]