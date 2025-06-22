import os
from dotenv import load_dotenv
from typing import List, Tuple
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()
# llm = ChatOpenAI(model_name="gpt-4", temperature=0)

# this is cheaper and less rate limit. If you have got premium, for gpt-4
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

embeddings = OpenAIEmbeddings()

def create_vector_store_from_texts_with_sources(texts, save_path="vector_db")

    # FAISS vector store
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

def load_vector_store(save_path="vector_db"):
    return FAISS.load_local(save_path, embeddings)

def retrieve_context(claim, vectorstore, k = 5):
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    return retriever.get_relevant_documents(claim)

def build_prompt(claim, documents):
    context = "\n\n".join([f"[{i+1}] ({doc.metadata.get('source', 'N/A')})\n{doc.page_content}" for i, doc in enumerate(documents)])
    template = f"""
You are a fact-checking assistant.

You are given a claim and context snippets from trusted sources (BBC, Reuters, Wikipedia, WHO, etc).

Determine if the claim is:
- TRUE
- FALSE
- MISLEADING

Cite the most relevant source(s) using the numbers provided.

---

Claim:
{claim}

---

Context:
{context}

---

Respond with:
Verdict: (True / False / Misleading)
Explanation:
Sources: [1], [2], etc.
"""
    return template

def verify_claim_with_citations(claim, vectorstore):
    documents = retrieve_context(claim, vectorstore)
    prompt = build_prompt(claim, documents)
    response = llm.predict(prompt)
    return response, documents
