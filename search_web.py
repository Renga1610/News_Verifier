# search/search_web.py

from duckduckgo_search import DDGS


# Search using duck-duck go. for better results, we can try with google search api
def search_web(query, max_results= 5):
    urls = []
    with DDGS() as ddgs:
        results = ddgs.text(query, region="wt-wt", safesearch="Moderate", max_results=max_results)
        for result in results:
            url = result.get("href")
            if url and any(source in url for source in ["bbc", "reuters", "wikipedia", "cnn", "nature.com", "who.int"]):
                urls.append(url)
    return urls
