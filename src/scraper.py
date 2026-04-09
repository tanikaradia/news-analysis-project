import requests
from bs4 import BeautifulSoup
import json

def fetch_news():
    url = "http://feeds.bbci.co.uk/news/rss.xml"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "xml") 

    articles = []

    for item in soup.find_all("item"): #item: article obj/ XML tag
        title = item.title.text #tags
        link = item.link.text

        articles.append({
            "title": title,
            "summary": "",
            "source": "BBC",
            "link": link
        })
        #HTML scraping ❌ (hard), Now: structured data (RSS)

    return articles


if __name__ == "__main__": #direct file run
    news = fetch_news()

    # for i in news[:5]:
    #     print(i)
    with open("data/news.json", "w") as f:
        json.dump(news, f, indent=4) #convert into JSON file and formatting

    print("Saved successfully")
    print(len(news))