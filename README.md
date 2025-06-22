The intention was to create a application to verify claims and news. This project is under construction.

If you are re-using/forking this project, create an OPENAI API key for yourself and add it in your environment.

Architecture:
1. User Input
2. Web Search (DuckDuckGo)
3. Top N Article URLs (BBC, Wikipedia, Reuters, etc.)
4. Web Scraper (newspaper3k / requests-html)
5. Text Cleaner + Chunker
6. Embedding Model (OpenAI or HuggingFace)
7. Vector Store (FAISS)
8. Retriever (LangChain)
9. GPT-4 (RAG prompt: claim + evidence)
10. Final Verdict (True / False / Misleading + explanation)

Cons:

1. DuckDuckGo search is not very reliable. Google API can do this better.
2. GPT-4 will hit rate limit quickly. I am preparing an Ollama based off-line model for local purpose.
3. UI/UX of streamlit app needs to be enhanced.
