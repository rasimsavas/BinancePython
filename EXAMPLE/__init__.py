# -*- coding: utf-8 -*-
from binance.client import Client
from datetime import datetime
import settings
import os

class Trader:
    BIDS = 'bids'
    ASKS = 'asks'
    def __init__(self):
        self.client = Client(str(os.getenv("API_PUBLIC")), str(os.getenv("API_SECRET")))
    
    def getPrices(self, currency=''):
        LIST = {}
        response = self.client.get_all_tickers()
        if isinstance(currency, list):
            for i in response:
                if i['symbol'] in currency:
                    LIST[i['symbol']] = i
        else:
            for i in response:
                if(str(i['symbol']).endswith(str(currency))):
                    LIST[i['symbol']] = i
        return LIST
    
    def getOrderBook(self, islem='',exc=''):
        if exc == '':
            liste = []
            book = self.client.get_order_book(symbol=islem)
            return book
        else:
            liste = []
            book = self.client.get_order_book(symbol=islem)
            for i in book[exc]:
                liste.append(i)
            return {"lastUpdateId":book['lastUpdateId'],exc:liste}
        
    def getVolume(self, currency):
        '''
        depth = self.client.get_order_book(symbol=currency)
        trades = self.client.get_recent_trades(symbol=currency)
        historical = self.client.get_historical_trades(symbol=currency)
        aggregate = self.client.get_aggregate_trades(symbol=currency) = start_symbol_ticker_socket
        '''
        price = self.client.get_ticker(symbol=currency)
        return price
        #return {"depth":depth, "trades":trades, "historical":historical, "aggregate":aggregate}
        
    def getCandlesticks(self, currency, minute = 15, startDate = '', endDate = ''):
        candle = []
        if startDate == '':
            switch = {
                1: Client.KLINE_INTERVAL_1MINUTE,
                5: Client.KLINE_INTERVAL_5MINUTE,
                15: Client.KLINE_INTERVAL_15MINUTE,
                30: Client.KLINE_INTERVAL_30MINUTE,
                60: Client.KLINE_INTERVAL_1HOUR,
                120: Client.KLINE_INTERVAL_2HOUR,
                240: Client.KLINE_INTERVAL_4HOUR,
                480: Client.KLINE_INTERVAL_8HOUR,
                1440: Client.KLINE_INTERVAL_1DAY,
            }
            candle = self.client.get_klines(symbol=currency, interval=switch.get(minute, lambda: Client.KLINE_INTERVAL_15MINUTE))
        else:
            switch = {
                1: Client.KLINE_INTERVAL_1DAY,
                3: Client.KLINE_INTERVAL_3DAY,
                7: Client.KLINE_INTERVAL_1WEEK,
                30: Client.KLINE_INTERVAL_1MONTH,
            }
            candle = self.client.get_historical_klines(symbol=currency, interval=switch.get(minute, lambda: Client.KLINE_INTERVAL_1WEEK))
        return candle[20:500]
    
    def getTimeData(self, currency, minute=1):
        candles = self.getCandlesticks(currency,minute) 
        dates = []
        open_data = []
        high_data = []
        low_data = []
        close_data = []
        
        for candle in candles:
            dates.append(datetime.fromtimestamp(candle[0] / 1000.0).strftime('%Y-%m-%d %H:%M:%S.%f'))
            open_data.append(float(candle[1]))
            high_data.append(float(candle[2]))
            low_data.append(float(candle[3]))
            close_data.append(float(candle[4]))
        volume = self.getVolume(currency)
        return {"dates":dates,"open":open_data,"close":close_data,"high":high_data,"low":low_data,"volume":volume}