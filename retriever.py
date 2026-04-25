from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from config import *

embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def load_db():
    return FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )


def retrieve(query, filter_type=None):
    db = load_db()

    docs_with_scores = db.similarity_search_with_score(query, k=5)

    # keep all top results (safer than strict filtering)
    filtered_docs = [doc for doc, score in docs_with_scores]

    # metadata filtering
    if filter_type:
        filtered_docs = [
            d for d in filtered_docs if d.metadata.get("type") == filter_type
        ]

    return filtered_docs