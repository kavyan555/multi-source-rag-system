from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from config import *

embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def load_db():
    return FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)


def retrieve(query, filter_type=None):
    db = load_db()

    docs = db.similarity_search(query, k=5)

    # 🔥 METADATA FILTERING
    if filter_type:
        docs = [d for d in docs if d.metadata.get("type") == filter_type]

    return docs