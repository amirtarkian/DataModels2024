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

    # gathering data from api
    def fetch_news(self, ticker, date):

        published_after = date
        published_before = (datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
        url = f"https://api.marketaux.com/v1/news/all?api_token={self.api_token}&symbols={ticker}&published_after={published_after}&published_before={published_before}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            sentiment_score = self.calculate_sentiment(data)
            return sentiment_score
        else:
            print("Failed to fetch news on", date, ":", response.status_code)


    # all this method is doing is finding the average scores, wonder if there would be a better way to compute the sentiment metric
    def calculate_sentiment(self, data):
        total_sentiment_score = 0
        sentiment_count = 0

        for article in data.get('data', []):
            for entity in article.get('entities', []):
                sentiment_score = entity.get('sentiment_score', None)
                if sentiment_score is not None:
                    total_sentiment_score += sentiment_score
                    sentiment_count += 1

        if sentiment_count > 0:
            print(f"Sentiment Score:{sentiment_score} with {sentiment_count} articles")
            return total_sentiment_score / sentiment_count
        else:
            print("No valid sentiment data available for this day.")
            

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


news = Sentiment()
ticker = 'AAPL' 
start_date = datetime(2016, 1, 4)  
end_date = datetime.today()  

sentiment_data = {}

current_date = start_date
while current_date <= end_date:
    date_str = current_date.strftime("%Y-%m-%d")
    sentiment_score = news.fetch_news(ticker, date_str)
    sentiment_data[date_str] = sentiment_score
    print(f"Sentiment score for {ticker} on {date_str}: {sentiment_score}")
    current_date += timedelta(days=1)

# trying to save this to a json because we have a daily limit for the api
save_to_json(sentiment_data, f"{ticker}_sentiment_data.json")
