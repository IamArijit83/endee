from fastapi import FastAPI, UploadFile, File, Form
from rag import add_documents, generate_answer
from utils import read_pdf, chunk_text
import shutil
import os

app = FastAPI()

UPLOAD_DIR = "data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# =========================
# ROOT (simple check)
# =========================
@app.get("/")
def home():
    return {"message": "RAG API running"}

# =========================
# UPLOAD
# =========================
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if file.filename.endswith(".pdf"):
        text = read_pdf(file_path)
    else:
        with open(file_path, encoding="utf-8") as f:
            text = f.read()

    chunks = chunk_text(text)
    add_documents(chunks)

    return {
        "message": "File processed",
        "chunks": len(chunks)
    }

# =========================
# ASK (RAG)
# =========================
@app.post("/ask")
def ask_question(query: str = Form(...)):
    answer = generate_answer(query)

    return {
        "query": query,
        "answer": answer
    }