# -*- coding: utf-8 -*-
from binance.client import Client
from datetime import datetime
import settings
import numpy as np
import talib as ta
from statistics import mean
import os

class Trader:
    BIDS = 'bids'
    ASKS = 'asks'
    FIBONACCI_VALUES = [23.6, 38.2, 50.0, 61.8, 78.6]
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
    
    def getTimeData(self, currency, minute=1, step=15):
        coin = {}
        coin.update(self.getVolume(currency))
        coin.update({
            "STEP":step,
            "RANGE":0,
            "DATES":{"DATA":[],"COUNT":0},
            "OPEN": {"DATA":[],"COUNT":0},
            "CLOSE":{"DATA":[],"COUNT":0}, 
            "HIGH":{"DATA":[],"COUNT":0}, 
            "LOW":{"DATA":[],"COUNT":0}, 
            "FIBONACCI":{"DATA":[],"COUNT":0},
            "TA":{},
        })
        candles = self.getCandlesticks(currency,minute)
        for candle in candles:
            #coin["DATES"]["DATA"].append(datetime.fromtimestamp(candle[0] / 1000.0).strftime('%Y-%m-%d %H:%M'))
            coin["DATES"]["DATA"].append(candle[0])
            coin["OPEN"]["DATA"].append(float(candle[1]))
            coin["CLOSE"]["DATA"].append(float(candle[2]))
            coin["HIGH"]["DATA"].append(float(candle[3]))
            coin["LOW"]["DATA"].append(float(candle[4]))
        coin["DATES"]["COUNT"] = len(coin["DATES"]["DATA"])
        coin["RANGE"] = int(coin["DATES"]["COUNT"]/coin["STEP"])
        coin["DATES"].update({
            "COUNT":len(coin["DATES"]["DATA"]),
            "MIN":min(coin["DATES"]["DATA"]),
            "MAX":max(coin["DATES"]["DATA"]),
            "AVG":[mean(coin["DATES"]["DATA"][(coin["STEP"]*i):(coin["STEP"]*(i+1))-1]) for i in range(coin["RANGE"])],
            "FULL_DATE":[(datetime.fromtimestamp(i / 1000.0).strftime('%Y-%m-%d %H:%M')) for i in coin["DATES"]["DATA"]],

        })
        coin["OPEN"].update({
            "COUNT":len(coin["OPEN"]["DATA"]),
            "MIN":min(coin["OPEN"]["DATA"]),
            "MAX":max(coin["OPEN"]["DATA"]),
            "AVG":[mean(coin["OPEN"]["DATA"][(coin["STEP"]*i):(coin["STEP"]*(i+1))-1]) for i in range(coin["RANGE"])],
        })
        coin["CLOSE"].update({
            "COUNT":len(coin["CLOSE"]["DATA"]),
            "MIN":min(coin["CLOSE"]["DATA"]),
            "MAX":max(coin["CLOSE"]["DATA"]),
            "AVG":[mean(coin["CLOSE"]["DATA"][(coin["STEP"]*i):(coin["STEP"]*(i+1))-1]) for i in range(coin["RANGE"])],
        })
        coin["HIGH"].update({
            "COUNT":len(coin["HIGH"]["DATA"]),
            "MIN":min(coin["HIGH"]["DATA"]),
            "MAX":max(coin["HIGH"]["DATA"]),
            "AVG":[mean(coin["HIGH"]["DATA"][(coin["STEP"]*i):(coin["STEP"]*(i+1))-1]) for i in range(coin["RANGE"])],
        })
        coin["LOW"].update({
            "COUNT":len(coin["LOW"]["DATA"]),
            "MIN":min(coin["LOW"]["DATA"]),
            "MAX":max(coin["LOW"]["DATA"]),
            "AVG":[mean(coin["LOW"]["DATA"][(coin["STEP"]*i):(coin["STEP"]*(i+1))-1]) for i in range(coin["RANGE"])],
        })
        coin["FIBONACCI"].update({
            "DATA": {
                "ASC":[[(float(max(coin["HIGH"]["DATA"][(coin["STEP"]*j):(coin["STEP"]*(j+1))-1]) - float(max(coin["HIGH"]["DATA"][(coin["STEP"]*j):(coin["STEP"]*(j+1))-1])-min(coin["LOW"]["DATA"][(coin["STEP"]*j):(coin["STEP"]*(j+1))-1])) * float(i/100))) for i in self.FIBONACCI_VALUES] for j in range(coin["RANGE"])],
                "DESC":[[(float(min(coin["LOW"]["DATA"][(coin["STEP"]*j):(coin["STEP"]*(j+1))-1]) + float(max(coin["HIGH"]["DATA"][(coin["STEP"]*j):(coin["STEP"]*(j+1))-1])-min(coin["LOW"]["DATA"][(coin["STEP"]*j):(coin["STEP"]*(j+1))-1])) * float(i/100))) for i in self.FIBONACCI_VALUES] for j in range(coin["RANGE"])],
            },
            "MAX":[(float(max(coin["HIGH"]["DATA"][(coin["STEP"]*j):(coin["STEP"]*(j+1))-1]))) for j in range(coin["RANGE"])],
            "MIN":[(float(min(coin["LOW"]["DATA"][(coin["STEP"]*j):(coin["STEP"]*(j+1))-1]))) for j in range(coin["RANGE"])],
            "HIGH_LOW_AVG":[(float((mean(coin["HIGH"]["DATA"][(coin["STEP"]*j):(coin["STEP"]*(j+1))-1])+mean(coin["LOW"]["DATA"][(coin["STEP"]*j):(coin["STEP"]*(j+1))-1]))/2)) for j in range(coin["RANGE"])],
            "OPEN_CLOSE_AVG":[(float((mean(coin["OPEN"]["DATA"][(coin["STEP"]*j):(coin["STEP"]*(j+1))-1])+mean(coin["CLOSE"]["DATA"][(coin["STEP"]*j):(coin["STEP"]*(j+1))-1]))/2)) for j in range(coin["RANGE"])],
            "START_DATE":[((datetime.fromtimestamp(min(coin["DATES"]["DATA"][(coin["STEP"]*j):(coin["STEP"]*(j+1))-1]) / 1000.0)).strftime('%Y-%m-%d %H:%M:%S.%f')) for j in range(coin["RANGE"])],
            "END_DATE":[((datetime.fromtimestamp(max(coin["DATES"]["DATA"][(coin["STEP"]*j):(coin["STEP"]*(j+1))-1]) / 1000.0)).strftime('%Y-%m-%d %H:%M:%S.%f')) for j in range(coin["RANGE"])],
        })
        coin["FIBONACCI"].update({
            "COUNT":len(coin["FIBONACCI"]["MAX"])
        })
        temp = {"CLOSE_FINISHED_ARRAY":coin["CLOSE"]["DATA"][:-1]}
        coin["TA"]["MACD"], coin["TA"]["MACD_SIGNAL"], coin["TA"]["MACD_HISTOGRAM"] = ta.MACD(np.asarray(temp["CLOSE_FINISHED_ARRAY"]))
        coin["TA"]["RSI"] = ta.RSI(np.asarray(temp["CLOSE_FINISHED_ARRAY"]))
        coin["TA"]["MACD"] = coin["TA"]["MACD"].tolist()
        coin["TA"]["MACD_SIGNAL"] = coin["TA"]["MACD_SIGNAL"].tolist()
        coin["TA"]["MACD_HISTOGRAM"] = coin["TA"]["MACD_HISTOGRAM"].tolist()
        coin["TA"]["RSI"] = coin["TA"]["RSI"].tolist()
        coin["TA"]["MACD"] = {
            "DATA":coin["TA"]["MACD"], 
            "COUNT":len(coin["TA"]["MACD"]),
            "MIN":np.nanmin(coin["TA"]["MACD"]),
            "MAX":np.nanmax(coin["TA"]["MACD"]),
            "LAST":coin["TA"]["MACD"][-1],
            "PREV":coin["TA"]["MACD"][-2]
        }
        coin["TA"]["MACD_HISTOGRAM"] = {
            "DATA":coin["TA"]["MACD_HISTOGRAM"], 
            "COUNT":len(coin["TA"]["MACD_HISTOGRAM"]),
            "MIN":np.nanmin(coin["TA"]["MACD_HISTOGRAM"]),
            "MAX":np.nanmax(coin["TA"]["MACD_HISTOGRAM"]),
            "LAST":coin["TA"]["MACD_HISTOGRAM"][-1],
            "PREV":coin["TA"]["MACD_HISTOGRAM"][-2]
        }
        coin["TA"]["MACD_SIGNAL"] = {
            "DATA":coin["TA"]["MACD_SIGNAL"], 
            "COUNT":len(coin["TA"]["MACD_SIGNAL"]),
            "MIN":np.nanmin(coin["TA"]["MACD_SIGNAL"]),
            "MAX":np.nanmax(coin["TA"]["MACD_SIGNAL"]),
            "LAST":coin["TA"]["MACD_SIGNAL"][-1],
            "PREV":coin["TA"]["MACD_SIGNAL"][-2]
        }
        coin["TA"]["RSI"] = {
            "DATA":coin["TA"]["RSI"], 
            "COUNT":len(coin["TA"]["RSI"]),
            "MIN":np.nanmin(coin["TA"]["RSI"]),
            "MAX":np.nanmax(coin["TA"]["RSI"]),
            "LAST":coin["TA"]["RSI"][-1],
            "PREV":coin["TA"]["RSI"][-2]
        }
        coin["TA"]["MACD_CROSS_UP"] = coin["TA"]["MACD"]["LAST"] > coin["TA"]["MACD_SIGNAL"]["LAST"] and coin["TA"]["MACD"]["PREV"] < coin["TA"]["MACD_SIGNAL"]["PREV"]
        coin["TA"]["MACD_CROSS_DOWN"] = coin["TA"]["MACD"]["LAST"] < coin["TA"]["MACD_SIGNAL"]["LAST"] and coin["TA"]["MACD"]["PREV"] > coin["TA"]["MACD_SIGNAL"]["PREV"]
        return coin