import requests
from bs4 import BeautifulSoup
import json
from analyzer import get_sentiment, classify_category, get_final_sentiment

def fetch_news():
    RSS_FEEDS = [
    "https://news.google.com/rss/search?q=government+india",
    "http://feeds.bbci.co.uk/news/rss.xml"
    ] # Really Simple Syndication

    articles = []

    for url in RSS_FEEDS:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "xml")

        for item in soup.find_all("item"):
            title = item.title.text
            title = title.replace("Watch:", "").strip()
            link = item.link.text

            summary = item.description.text if item.description else ""

            sentiment = get_final_sentiment(title, summary)
            category = classify_category(title + " " + summary)

            articles.append({
                "title": title,
                "link": link,
                "category": category,
                "sentiment": sentiment,
            })

    unique_articles = []
    seen = set() # Duplication Filter: store title already seen/ 

    for article in articles:
        if article["title"] not in seen:
            unique_articles.append(article)
            seen.add(article["title"])

    return unique_articles
