from app.services.llm_service import askLLM

async def extractResumeData(text: str):
    prompt = f"""
You are a Resume-parser. Extract ONLY name, email, skills, expeirience and degrees from the following text:
{text}
Give the result as JSON back.
"""
    result = await askLLM(prompt)
    return result