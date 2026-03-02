from fastapi import APIRouter, UploadFile, File
import tempfile
from pypdf import PdfReader
import io

from app.services.resume_parser import extractTextFromPdf
from app.services.llm_service import llm

router = APIRouter(prefix="/resume", tags=["resume"])

@router.get("/")
def test():
    return{"message": "Resume route works"}

@router.post("/upload")
async def uploadResume(file:UploadFile = File(...)):
    content = await file.read()
    print(f"Received file: {file.filename}, size: {len(content)} bytes")
    return {"filename": file.filename, "size": len(content)}

@router.post("/extract-text")
async def extractText(file: UploadFile = File(...)):
    fileBytes = await file.read()
    fileLike = io.BytesIO(fileBytes)
    reader = PdfReader(fileLike)

    fullText = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            fullText += text + "\n"

    return {"text": fullText}