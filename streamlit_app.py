# streamlit_app.py

import streamlit as st
from search_web import search_web
from scraper import scrape_articles
from vector.embed_store import create_vector_store_from_texts_with_sources
from verifier import verify_claim_with_citations

from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="News Verifier Bot", layout="wide")
st.title("RAG-Powered News Verifier Bot")
st.caption("Check claims using GPT and live data from trusted sources")

with st.form("claim_form"):
    claim = st.text_input("Enter a factual claim to verify:", "")
    submitted = st.form_submit_button("Verify")

if submitted and claim:
    with st.spinner("Searching, scraping, embedding, verifying..."):
        urls = search_web(claim)
        if not urls:
            st.error("No articles found.")
        else:
            raw_articles = scrape_articles(urls)
            url_texts = list(zip(urls, raw_articles))
            vectorstore = create_vector_store_from_texts_with_sources(url_texts)
            response, docs = verify_claim_with_citations(claim, vectorstore)

            st.success("✅ Verification complete")
            st.subheader("Verdict")
            st.markdown(f"```text\n{response}\n```")

            st.subheader("📚 Sources & Context")
            for i, doc in enumerate(docs):
                st.markdown(f"**[{i+1}] Source:** [{doc.metadata['source']}]({doc.metadata['source']})")
                st.markdown(f"> {doc.page_content[:500]}...")

st.markdown("---")
st.caption("Built with LangChain, FAISS, GPT-4, and Streamlit")
