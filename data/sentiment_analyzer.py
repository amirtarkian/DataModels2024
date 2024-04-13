""" 

link: https://www.marketaux.com/account/dashboard
Username: ryanflatley0@gmail.com
Password: 2022wuwu5RF!

 """

import requests
import json
from datetime import datetime, timedelta

class Sentiment:
    def __init__(self):
        self.api_token = 'VbpPND1Ic1JnfJW2ms9IpAS9b3NE4xh76zWxanA6'

    def fetch_news(self, ticker, start_date, end_date):
        # Prepare date formatting for the API request
        published_after = start_date.strftime("%Y-%m-%d")
        published_before = end_date.strftime("%Y-%m-%d")

        # Construct the URL with all necessary parameters
        url = f"https://api.marketaux.com/v1/news/all?symbols={ticker}&filter_entities=true&language=en&api_token={self.api_token}&published_after={published_after}&published_before={published_before}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            sentiment_score = self.calculate_sentiment(data)
            return sentiment_score
        else:
            print(f"Failed to fetch news between {published_after} and {published_before}: {response.status_code}")

    def calculate_sentiment(self, data):
        total_sentiment_score = 0
        sentiment_count = 0

        # Calculate the average sentiment score from the data received
        for article in data.get('data', []):
            for entity in article.get('entities', []):
                sentiment_score = entity.get('sentiment_score', None)
                if sentiment_score is not None:
                    total_sentiment_score += sentiment_score
                    sentiment_count += 1

        if sentiment_count > 0:
            return total_sentiment_score / sentiment_count
        else:
            print("No valid sentiment data available.")

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def main():
    news = Sentiment()
    ticker = 'AAPL'
    start_date = datetime.today() - timedelta(days=6)  # Adjust the days as needed
    end_date = datetime.today()

    sentiment_data = {}
    current_date = start_date
    while current_date <= end_date:
        sentiment_score = news.fetch_news(ticker, start_date, current_date)
        date_str = current_date.strftime("%Y-%m-%d")
        sentiment_data[date_str] = sentiment_score
        print(f"Sentiment score for {ticker} up to {date_str}: {sentiment_score}")
        current_date += timedelta(days=1)

    save_to_json(sentiment_data, f"{ticker}_sentiment_data.json")

if __name__ == "__main__":
    main()
