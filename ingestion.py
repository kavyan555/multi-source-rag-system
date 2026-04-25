import os
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_core.documents import Document
from bs4 import BeautifulSoup
import requests

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import *


# ---------- LOADERS ----------

def load_pdfs(folder):
    docs = []
    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(folder, file))
            data = loader.load()
            for d in data:
                d.metadata["source"] = file
                d.metadata["type"] = "pdf"
            docs.extend(data)
    return docs


def load_docx(folder):
    docs = []
    for file in os.listdir(folder):
        if file.endswith(".docx"):
            loader = Docx2txtLoader(os.path.join(folder, file))
            data = loader.load()
            for d in data:
                d.metadata["source"] = file
                d.metadata["type"] = "docx"
            docs.extend(data)
    return docs


def load_csv(folder):
    docs = []
    for file in os.listdir(folder):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(folder, file))
            for _, row in df.iterrows():
                docs.append(Document(
                    page_content=f"Region: {row['region']}, Product: {row['product']}, Revenue: {row['revenue']}, Month: {row['month']}",
                    metadata={"source": file, "type": "csv"}
                ))
    return docs


def load_web(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text()
    return [Document(page_content=text, metadata={"source": url, "type": "web"})]


# ---------- PROCESSING ----------

def process_and_store(all_docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = splitter.split_documents(all_docs)

    # remove duplicates
    unique_chunks = list({c.page_content: c for c in chunks}.values())

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    db = FAISS.from_documents(unique_chunks, embeddings)

    db.save_local(VECTOR_DB_PATH)

    print("✅ Vector DB created")

if __name__ == "__main__":
    docs = []
    docs += load_pdfs("data/pdfs")
    docs += load_docx("data/docs")
    docs += load_csv("data/csvs")

    print(f"Loaded {len(docs)} documents")

    process_and_store(docs)