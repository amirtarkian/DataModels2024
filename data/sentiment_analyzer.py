""" 

link: https://www.marketaux.com/account/dashboard
Username: ryanflatley0@gmail.com
Password: 2022wuwu5RF!

 """

import requests
import json
from datetime import datetime, timedelta

import requests
import json
from datetime import datetime, timedelta

# API Token should be kept secure and not hardcoded in production
API_TOKEN = 'VbpPND1Ic1JnfJW2ms9IpAS9b3NE4xh76zWxanA6'

def fetch_news(ticker, start_date, end_date):
    published_after = start_date.strftime("%Y-%m-%d")
    published_before = (end_date + timedelta(days=1)).strftime("%Y-%m-%d")

    url = f"https://api.marketaux.com/v1/news/all?symbols={ticker}&filter_entities=true&language=en&api_token={API_TOKEN}&published_after={published_after}&published_before={published_before}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        sentiment_score = calculate_sentiment(data)
        return sentiment_score
    else:
        print(f"Failed to fetch news between {published_after} and {published_before}: {response.status_code}")
        return None

def calculate_sentiment(data):
    total_sentiment_score = 0
    sentiment_count = 0

    for article in data.get('data', []):
        for entity in article.get('entities', []):
            sentiment_score = entity.get('sentiment_score', None)
            if sentiment_score is not None:
                total_sentiment_score += sentiment_score
                sentiment_count += 1

    if sentiment_count > 0:
        return total_sentiment_score / sentiment_count
    else:
        return None

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

ticker = 'AAPL'
end_date =datetime(2023, 10, 27)
# start_date = end_date - timedelta(days=86)
start_date = datetime(2023,9,30)

sentiment_data = {}
last_valid_sentiment = 0.00

current_date = start_date
while current_date <= end_date:
    sentiment_score = fetch_news(ticker, start_date, current_date)
    date_str = current_date.strftime("%Y-%m-%d")
    if sentiment_score is not None:
        sentiment_data[date_str] = sentiment_score
        last_valid_sentiment = sentiment_score
    else:
        sentiment_data[date_str] = last_valid_sentiment  # Use last valid sentiment if current is none or null
    print(f"Sentiment score for {ticker} up to {date_str}: {sentiment_data[date_str]}")
    current_date += timedelta(days=1)

save_to_json(sentiment_data, f"{ticker}_cumulative_sentiment_data.json")
