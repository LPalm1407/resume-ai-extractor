from fastapi import FastAPI
from app.routes.resume import router as resume_router
from app.services.resume_service import extractResumeData
from app.routes import llmTest
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume_router)
app.include_router(llmTest.router)

@app.post("/resumeextract-text")
async def extractTextEndpoint(text: str):
    parsed = await extractResumeData(text)
    return {"parsed": parsed}