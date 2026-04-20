# services/vector_store.py

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_community.embeddings import OllamaEmbeddings


def build_vector_store(texts):
    embeddings = OllamaEmbeddings(model="llama3")

    docs = [Document(page_content=t) for t in texts]

    vector_db = FAISS.from_documents(docs, embeddings)

    return vector_db