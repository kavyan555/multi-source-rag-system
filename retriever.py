from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from config import VECTOR_DB_PATH, EMBEDDING_MODEL


# ✅ initialize embeddings once
embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)


# ✅ load vector DB
def load_db():
    return FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )


# ✅ main retrieval function
def retrieve(query, department=None, k=5):
    db = load_db()

    docs_with_scores = db.similarity_search_with_score(query, k=k)
    docs = [doc for doc, score in docs_with_scores]

    if department and department != "All":
        docs = [
            d for d in docs
            if d.metadata.get("department") == department
        ]

    return docs