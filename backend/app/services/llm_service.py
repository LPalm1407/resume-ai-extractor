import httpx
import json
from app.core.config import OLLAMA_URL, OLLAMA_MODEL

async def askLLM(prompt: str):
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "temperature": 0.7,
        "stream": True  
    }

    full_response = ""

    async with httpx.AsyncClient(timeout=60.0) as client:
        async with client.stream("POST", OLLAMA_URL + "/api/generate", json=payload) as response:
            print("Status:", response.status_code)
            response.raise_for_status()

            async for line in response.aiter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        text = chunk.get("response", "")
                        full_response += text
                        print(text, end="", flush=True)
                    except json.JSONDecodeError:
                        continue

    return full_response