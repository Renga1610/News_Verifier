import os
from dotenv import load_dotenv
from typing import List
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from typing import List, Tuple
from langchain.schema import Document
from langchain.embeddings import OpenAIEmbeddings

from dotenv import load_dotenv
load_dotenv()

embeddings = OpenAIEmbeddings()


# Load environment variables
load_dotenv()

# Initialize embeddings
embeddings = OpenAIEmbeddings()

def chunk_documents(texts, chunk_size=500, chunk_overlap=50):
    """
    Takes list of raw article texts and splits them into Documents.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = []
    for text in texts:
        docs.extend(splitter.create_documents([text]))
    return docs

def create_vector_store_from_texts(texts, save_path: str = "vector_db"):
    """
    Creates a FAISS vector store from raw article texts and saves to disk.
    """
    chunks = chunk_documents(texts)
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(save_path)
    return vectorstore

def create_vector_store_from_texts_with_sources(texts, save_path="vector_db"):
    """
    Creates FAISS vector store with documents that include metadata for source URLs.
    texts = List of (url, article_text)
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    all_docs = []
    for url, text in texts:
        docs = splitter.create_documents([text])
        for doc in docs:
            doc.metadata = {"source": url}
        all_docs.extend(docs)

    vectorstore = FAISS.from_documents(all_docs, embeddings)
    vectorstore.save_local(save_path)
    return vectorstore


def load_vector_store(save_path: str = "vector_db"):
    """
    Loads a previously saved FAISS vector store.
    """
    return FAISS.load_local(save_path, embeddings)

def get_top_k_chunks(query, vectorstore, k: int = 5):
    """
    Retrieves top-K most relevant chunks for a given query.
    """
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    results = retriever.get_relevant_documents(query)
    return [doc.page_content for doc in results]
