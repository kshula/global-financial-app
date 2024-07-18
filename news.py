import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_yahoo_finance_news(pages=5):
    base_url = "https://finance.yahoo.com/news/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    all_articles = []

    for page in range(1, pages + 1):
        url = f"{base_url}?p={page}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        articles = soup.find_all("li", class_="js-stream-content")

        for article in articles:
            try:
                title = article.find("h3").get_text(strip=True)
                link = article.find("a")["href"]
                if not link.startswith("https"):
                    link = "https://finance.yahoo.com" + link
                date = article.find("time")["datetime"]
                all_articles.append({"title": title, "date": date, "link": link})
            except Exception as e:
                print(f"Error processing article: {e}")
                continue

        time.sleep(3)  # Be kind to the server and avoid getting blocked

    return all_articles

# Scrape news articles
news_articles = scrape_yahoo_finance_news(pages=5)  # Adjust the number of pages as needed

# Convert to DataFrame and save to CSV
df = pd.DataFrame(news_articles)
df.to_csv("financial_news_yahoo.csv", index=False)

print("Scraping complete. Data saved to financial_news_yahoo.csv")
