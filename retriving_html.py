import requests
import time
from fake_useragent import UserAgent

symbol = "AAPL"
base_url = f"https://query2.finance.yahoo.com/v1/finance/search"
session = requests.Session()
user_agent = UserAgent()

proxy_auth = '3dd0791cfcbc3a517688:cf9959e44274816b@144.76.124.83:823'
proxies = {
    "http": f"http://{proxy_auth}",
    "https": f"http://{proxy_auth}",
}

headers = {
    "Accept": "application/json",
    "User-Agent": user_agent.random
}

results = []

for page in range(20):  # Loop for 20 "pages"
    offset = page * 10  # Approx. 10 results per page
    params = {
        "q": symbol,
        "newsCount": "10",
        "quotesCount": "0",
        "enableFuzzyQuery": "false",
        "quotesQueryId": "tss_match_phrase_query",
        "newsQueryId": "news_cie_vespa",
        "enableCb": "false",
        "enableNavLinks": "false",
        "enableEnhancedTrivialQuery": "false",
        "start": str(offset)
    }

    try:
        response = session.get(base_url, headers=headers, proxies=proxies, params=params, timeout=10)
        response.raise_for_status()
        json_data = response.json()
        news_items = json_data.get("news", [])
        results.extend(news_items)
        print(f"Fetched page {page+1} with {len(news_items)} items")
        time.sleep(1)  # Sleep to avoid rate limiting
    except Exception as e:
        print(f"Error on page {page+1}: {e}")
        continue

# Save to a file
with open("aapl_news_data.txt", "w", encoding="utf-8") as f:
    for item in results:
        title = item.get("title", "N/A")
        link = item.get("link", "N/A")
        publisher = item.get("publisher", "N/A")
        pub_date = item.get("providerPublishTime", "N/A")
        f.write(f"{title}\n{link}\n{publisher}\n{pub_date}\n\n")

print(f"Total articles saved: {len(results)}")
