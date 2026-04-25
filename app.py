import streamlit as st
from ingestion import load_pdfs, load_docx, load_csv, process_and_store
from retriever import retrieve
from llm import ask_llm

st.title("📚 Multi-Document RAG Chatbot")

option = st.sidebar.selectbox("Choose Mode", ["Ingest", "Chat"])


# ---------- INGEST ----------
if option == "Ingest":
    if st.button("Process Documents"):
        docs = []
        docs += load_pdfs("data/pdfs")
        docs += load_docx("data/docs")
        docs += load_csv("data/csvs")

        process_and_store(docs)
        st.success("Documents indexed!")


# ---------- CHAT ----------
elif option == "Chat":
    query = st.text_input("Ask something")

    filter_type = st.selectbox(
        "Filter by type",
        ["All", "pdf", "docx", "csv", "web"]
    )

    if st.button("Ask"):

        if not query:
            st.warning("Please enter a question")
        else:
            docs = retrieve(query, None if filter_type == "All" else filter_type)

            if not docs:
                st.warning("No relevant documents found")
            else:
                # 🔥 limit context
                context = "\n".join([d.page_content for d in docs[:3]])

                answer = ask_llm(context, query)

                st.write("### Answer:")
                st.write(answer)

                st.write("### Sources:")

                # 🔥 remove duplicate sources
                seen = set()
                for d in docs:
                    source = d.metadata.get("source")
                    if source not in seen:
                        st.write(d.metadata)
                        seen.add(source)