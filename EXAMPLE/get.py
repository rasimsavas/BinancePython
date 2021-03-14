from binance.client import Client
import settings
import os

client = Client(str(os.getenv("API_PUBLIC")), str(os.getenv("API_SECRET")))

def getPrices(client, currency):
    client.get_all_tickers()
    LIST = []
    for i in info:
        if(str(i['symbol']).endswith(currency)):
            LIST.append(i)
    return LIST
    