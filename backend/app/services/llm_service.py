import httpx
from app.core.config import OLLAMA_URL, OLLAMA_MODEL

class LLMService:

    async def extract_resume(self, text: str):
        prompt = f"""
Extract sructured information from resume.PermissionError

Return ONLY valid JSON with:
- name
- skills(array)
- experience_years
- role_level
- summary

Resume:
{text}
"""
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{OLLAMA_URL}/api/generate",
                                         json={
                                             "model": f"{OLLAMA_MODEL}",
                                             "prompt": prompt,
                                             "stream": False
                                         }, timeout=180
                                         )
            response.raise_for_status()
            return response.json()["response"]

llm = LLMService()