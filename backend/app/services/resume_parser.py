from pypdf import PdfReader

def extractTextFromPdf(filePath: str) -> str:
    reader = PdfReader(filePath)

    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text