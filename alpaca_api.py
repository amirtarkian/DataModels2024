
""" 

link: https://app.alpaca.markets/account/login
Username: ryanflatley0@gmail.com
Password: 2022wuwu5RF!

 """


import alpaca_trade_api as tradeapi
from datetime import datetime
import pytz

# API credentials
api_key = 'AKQB26E5HLHLA54FOT9T'
api_secret = 'hNgAGISeVTThSFOoa1biaGcRuWYD8HvOvtb1AB7c'
base_url = 'https://paper-api.alpaca.markets'  

# Initialize the Alpaca API
api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

symbol = 'AAPL' 
start_date = datetime(2022, 1, 1).astimezone(pytz.timezone('UTC')) 
end_date = datetime(2022, 1, 31).astimezone(pytz.timezone('UTC'))  

daily_prices = api.get_bars(symbol, tradeapi.TimeFrame.Day, start_date.isoformat(), end_date.isoformat()).df

print(daily_prices)


