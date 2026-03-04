# app/routes/llm_test.py
from fastapi import APIRouter
import httpx
import json
from app.core.config import OLLAMA_URL, OLLAMA_MODEL

router = APIRouter()

@router.get("/test-llm")
async def test_llm():
    prompt = "Sag Hallo auf Deutsch."
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "temperature": 0.7,
        "stream": True  # wichtig: Streaming aktivieren
    }

    full_response = ""

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream("POST", f"{OLLAMA_URL}/api/generate", json=payload) as response:
                print("Statuscode:", response.status_code)

                async for line in response.aiter_lines():
                    if line:
                        try:
                            chunk = json.loads(line)
                            # Text zusammenfügen
                            full_response += chunk.get("response", "")
                            # Optional: live anzeigen
                            print(chunk.get("response", ""), end="", flush=True)
                        except json.JSONDecodeError:
                            # Manche Zeilen könnten leer oder fehlerhaft sein
                            continue

        return {"status": "ok", "response": full_response}

    except httpx.HTTPError as e:
        return {"status": "error", "detail": str(e)}
    except Exception as e:
        return {"status": "error", "detail": str(e)}