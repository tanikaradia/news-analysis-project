from scraper import fetch_news

def main():
    news = fetch_news()

    for article in news[:5]:
        print(article)

if __name__ == "__main__":
    main()