import requests
from bs4 import BeautifulSoup
import json
from analyzer import get_sentiment, classify_category, get_final_sentiment

def fetch_news():
    url = "http://feeds.bbci.co.uk/news/rss.xml"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "xml") 

    articles = []

    for item in soup.find_all("item"): #item: article obj/ XML tag
        title = item.title.text #tags
        title = title.replace("Watch:", "").strip() #remove Watch:
        link = item.link.text

        summary = item.description.text if item.description else "" #NoneType error if no descrpn
        # full_text = title + " " + title + " " + summary
        sentiment = get_final_sentiment(title, summary)
        category = classify_category(title + " " + summary)

        articles.append({
            "title": title,
            "link": link,
            "category": category,
            "sentiment": sentiment,
        })

    return articles

