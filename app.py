import os
import uuid
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from rag import ingest_pdf, ask as rag_ask

app = FastAPI()
os.makedirs("uploads", exist_ok=True)


class Question(BaseModel):
    question: str
    doc_id: str


@app.get("/")
def home():
    return FileResponse("index.html")


@app.post("/upload")
def upload(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF file")

    doc_id = uuid.uuid4().hex
    path = f"uploads/{doc_id}.pdf"
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    chunks = ingest_pdf(path, doc_id)
    return {"doc_id": doc_id, "filename": file.filename, "chunks": chunks}


@app.post("/ask")
def ask_question(q: Question):
    if not q.question.strip():
        raise HTTPException(status_code=400, detail="Question is empty")
    return {"answer": rag_ask(q.question, q.doc_id)}