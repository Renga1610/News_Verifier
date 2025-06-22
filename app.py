# app.py

from search_web import search_web
from scraper import scrape_articles
from vector.embed_store import create_vector_store_from_texts
from verifier import verify_claim

def fact_check_claim(claim: str):
    print(f"\n🔍 Searching the web for: {claim}")
    urls = search_web(claim)
    if not urls:
        print("❌ No trusted sources found.")
        return

    print(f"🌐 Found {len(urls)} URLs. Scraping articles...")
    articles = scrape_articles(urls)
    if not articles:
        print("❌ Failed to scrape any usable content.")
        return

    print(f"📦 Creating vector store from {len(articles)} articles...")
    create_vector_store_from_texts(articles)

    print("🤖 Asking GPT-4 to verify the claim...\n")
    response = verify_claim(claim)
    print("🧠 GPT-4 Verdict:\n", response)

if __name__ == "__main__":
    print("📢 Welcome to the RAG-Powered News Verifier Bot!")
    while True:
        claim = input("\n💬 Enter a claim to verify (or 'exit'): ")
        if claim.strip().lower() in ['exit', 'quit']:
            break
        fact_check_claim(claim)
