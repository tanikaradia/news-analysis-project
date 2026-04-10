from scraper import fetch_news

def main():
    news = fetch_news()

    import json

    with open("data/news.json", "w") as f:
        json.dump(news, f, indent=4)

    # for article in news[:5]:
    #     print(article)

if __name__ == "__main__":
    main() #direct exec no import