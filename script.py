import requests
from bs4 import BeautifulSoup

def run():
    print("🔗 Fetching Hacker News...")
    response = requests.get("https://news.ycombinator.com/")
    soup = BeautifulSoup(response.text, "html.parser")

    print("📰 Top 5 Headlines:")
    headlines = soup.select("a.titlelink")
    for i, link in enumerate(headlines[:5], start=1):
        print(f"{i}. {link.text}")

run()

