from bs4 import BeautifulSoup
import pandas as pd

# Read HTML
with open("file.html", "r", encoding="utf-8") as f:
    html = f.read()

# Parse HTML
soup = BeautifulSoup(html, "html.parser")

# Extract news blocks (each news is usually inside an <li> or <div>)
news_cards = soup.find_all("li")  # or soup.find_all("div", recursive=True)

# Prepare lists
dates, headlines, changes = [], [], []

for card in news_cards:
    date_div = card.find("div")
    headline_tag = card.find("h3")
    change_tag = card.find("span")

    if date_div and headline_tag and change_tag:
        dates.append(date_div.text.strip())
        headlines.append(headline_tag.text.strip())
        changes.append(change_tag.text.strip())

# Create DataFrame
df = pd.DataFrame({
    "Date": dates,
    "Headline": headlines,
    "stock_dec_incre": changes
})

print(df.head())
df.to_csv("stocks_sentiment.csv", index=False, encoding="utf-8")
