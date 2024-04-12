import os
import requests
from datetime import datetime, timedelta

""" 

link: https://www.marketaux.com/account/dashboard
Username: ryanflatley0@gmail.com
Password: 2022wuwu5RF!

 """

import os
import requests
from datetime import datetime, timedelta

class NewsSentiment:
    token = "VbpPND1Ic1JnfJW2ms9IpAS9b3NE4xh76zWxanA6"

    def __init__(self):
        self.api_token = self.token
        self.sentiment_range = ["0.1", "0.3", "0.31", "0.7", "0.71", "1"]
        self.sentiment_weight = [1, 2, 3]

    def fetch_news_and_calculate_sentiment(self, ticker):
        url_base = "https://api.marketaux.com/v1/news/all?api_token={}".format(self.api_token)
        days_range = 30
        urls = []

        for i in range(0, len(self.sentiment_range), 2):
            url = "{}&symbols={}&filter_entities=true&published_after={}&sentiment_gte={}&sentiment_lte={}".format(
                url_base, ticker, (datetime.today() - timedelta(days=days_range)).strftime("%Y-%m-%d"),
                self.sentiment_range[i], self.sentiment_range[i + 1])
            urls.append(url)
            url = "{}&symbols={}&filter_entities=true&published_after={}&sentiment_gte=-{}&sentiment_lte=-{}".format(
                url_base, ticker, (datetime.today() - timedelta(days=days_range)).strftime("%Y-%m-%d"),
                self.sentiment_range[i + 1], self.sentiment_range[i])
            urls.append(url)

        sentiment_score = self.compute_sentiment(urls)
        return sentiment_score

    def compute_sentiment(self, urls):
        sentiment_score = 0
        article_counts = {"positive": 0, "negative": 0}

        # Send requests
        for url in urls:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                for article in data['data']:
                    sentiment_value = article.get('sentiment')
                    if sentiment_value is not None:
                        try:
                            sentiment = float(sentiment_value)
                            index = self.get_weight_index(sentiment)
                            if sentiment > 0:
                                article_counts["positive"] += 1 * self.sentiment_weight[index]
                            elif sentiment < 0:
                                article_counts["negative"] += 1 * self.sentiment_weight[index]
                        except ValueError:
                            print("Invalid sentiment value:", sentiment_value)  
                            continue

        print("Article counts:", article_counts)  
        total_articles = article_counts["positive"] + article_counts["negative"]
        if total_articles > 0:
            sentiment_score = (article_counts["positive"] - article_counts["negative"]) / total_articles

        return sentiment_score

    def get_weight_index(self, sentiment):
        if sentiment >= 0.71 or sentiment <= -0.71:
            return 2  # Strong
        elif (sentiment >= 0.31 and sentiment <= 0.7) or (sentiment <= -0.31 and sentiment >= -0.7):
            return 1  # Moderate
        elif (sentiment >= 0.1 and sentiment <= 0.3) or (sentiment <= -0.1 and sentiment >= -0.3):
            return 0  # Weak
        return -1  

# Usage
news_sentiment = NewsSentiment()
score = news_sentiment.fetch_news_and_calculate_sentiment("AAPL")
print("Sentiment Score:", score)
