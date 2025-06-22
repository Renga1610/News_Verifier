# scrape/scraper.py

from newspaper import Article
import concurrent.futures
from typing import List, Tuple

# Scrapes a single news article and returns (url, cleaned_text)
def scrape_article(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        text = article.text
        if len(text) > 200:  # Ignore too-short pages
            return (url, text.strip())
    except Exception as e:
        print(f"❌ Failed to scrape {url}: {e}")
    return (url, "")

# Scrapes multiple articles in parallel and returns cleaned article texts.
# Multithreading to make it faster
def scrape_articles(urls: List[str]) -> List[str]:
    clean_articles = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(scrape_article, urls)
        for url, text in results:
            if text:
                clean_articles.append(text)
    return clean_articles
