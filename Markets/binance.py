import datetime
import os
from datetime import datetime
from statistics import mean
from Markets.helpers import minuteIntervalSwitch

import numpy as np
import talib as ta
from binance.client import Client


class Binance(Client):
    USDT = 'USDT'
    ETH = 'ETH'
    BIDS = 'bids'
    ASKS = 'asks'
    FIBONACCI_VALUES = [23.6, 38.2, 50.0, 61.8, 78.6]

    def __init__(self):
        super().__init__()
        self.api_key = str(os.getenv("BINANCE_API_KEY"))
        self.api_secret = str(os.getenv("BINANCE_SECRET_KEY"))

    def getPrices(self, currency=USDT):
        currency_list = {}
        response = self.get_all_tickers()
        if isinstance(currency, list):
            for i in response:
                if i['symbol'] in currency:
                    currency_list[i['symbol']] = float(i['price'])
        else:
            for i in response:
                if str(i['symbol']).endswith(str(currency)):
                    currency_list[i['symbol']] = float(i['price'])
        return currency_list

    def sendPing(self):
        return self.ping()

    def getServerTime(self):
        return self.get_server_time()

    def getSystemStatus(self):
        return self.get_system_status()

    def getExchangeInfo(self):
        return self.get_exchange_info()

    def getCurrencyInfo(self, currency=(ETH + USDT)):
        return self.get_symbol_info(symbol=currency)

    def getAllCoinsInfo(self):
        return self.get_all_tickers()

    def getMarketDepth(self, currency=(ETH + USDT)):
        return self.get_order_book(symbol=currency)

    def getRecentTrades(self, currency=(ETH + USDT)):
        return self.get_recent_trades(symbol=currency)

    def getHistoricalTrades(self, currency=(ETH + USDT)):
        return self.get_historical_trades(symbol=currency)

    def getAggregateTrades(self, currency=(ETH + USDT)):
        return self.get_aggregate_trades(symbol=currency)

    def getCandlesticks(self, currency=(ETH + USDT), interval='30m'):
        return self.get_klines(symbol=currency, interval=interval)

    def getHistoricalCandlesticks(self, currency=(ETH + USDT), interval='30m',
                                  start='08 Aug, 2021', end='23 Aug, 2021', limit=500):
        return self.get_historical_klines(symbol=currency, interval=interval, start_str=start, end_str=end, limit=limit)

    def getAveragePrice(self, currency=(ETH + USDT)):
        return self.get_avg_price(symbol=currency)

    def get24hrTicker(self, currency=(ETH + USDT)):
        info = self.get_ticker(symbol=currency)
        return {
            'symbol': info['symbol'],
            'priceChange': float(info['priceChange']),
            'priceChangePercent': float(info['priceChangePercent']),
            'weightedAvgPrice': float(info['weightedAvgPrice']),
            'prevClosePrice': float(info['prevClosePrice']),
            'lastPrice': float(info['lastPrice']),
            'lastQty': float(info['lastQty']),
            'bidPrice': float(info['bidPrice']),
            'bidQty': float(info['bidQty']),
            'askPrice': float(info['askPrice']),
            'askQty': float(info['askQty']),
            'openPrice': float(info['openPrice']),
            'highPrice': float(info['highPrice']),
            'lowPrice': float(info['lowPrice']),
            'volume': float(info['volume']),
            'quoteVolume': float(info['quoteVolume']),
            'openTime': 1629629528602,
            'closeTime': 1629715928602,
            'firstId': 572236110,
            'lastId': 573502594,
            'count': 1266485,
        }

    def getAllPrices(self):
        return self.get_all_tickers()

    def getOrderbookTickers(self):
        return self.get_orderbook_tickers()

    def getAssetDetails(self):
        return self.get_asset_details()

    def getAccount(self):
        return self.get_account()

    def getTimeData(self, currency=(ETH + USDT), minute=1, step=15):
        coin = {}
        coin.update(self.get24hrTicker(currency=currency))
        coin.update({
            "STEP": step,
            "RANGE": 0,
            "DATES": {"DATA": [], "COUNT": 0},
            "OPEN": {"DATA": [], "COUNT": 0},
            "CLOSE": {"DATA": [], "COUNT": 0},
            "HIGH": {"DATA": [], "COUNT": 0},
            "LOW": {"DATA": [], "COUNT": 0},
            "FIBONACCI": {"DATA": [], "COUNT": 0},
            "TA": {},
        })
        candles = self.getCandlesticks(currency=currency, interval=minuteIntervalSwitch(minute))[20:500]
        for candle in candles:
            coin.update({
                'DATES': {'DATA': coin['DATES']['DATA'] + [candle[0]]},
                'OPEN': {'DATA': coin['OPEN']['DATA'] + [float(candle[1])]},
                'CLOSE': {'DATA': coin['CLOSE']['DATA'] + [float(candle[2])]},
                'HIGH': {'DATA': coin['HIGH']['DATA'] + [float(candle[3])]},
                'LOW': {'DATA': coin['LOW']['DATA'] + [float(candle[4])]},
            })
        count = len(coin['DATES']['DATA'])
        coin.update({
            'DATES': {
                'COUNT': count,
                'DATA': coin['DATES']['DATA'],
                'MIN': min(coin['DATES']['DATA']),
                'MAX': min(coin['DATES']['DATA']),
                'AVG': [mean(coin["DATES"]["DATA"][(coin["STEP"] * i):(coin["STEP"] * (i + 1)) - 1]) for i in
                        range(coin['RANGE'])],
                "FULL_DATE": [(datetime.fromtimestamp(i / 1000.0).strftime('%Y-%m-%d %H:%M')) for i in
                              coin["DATES"]["DATA"]],
            },
            'OPEN': {
                'DATA': coin['OPEN']['DATA'],
                'COUNT': len(coin['OPEN']['DATA']),
                'MIN': min(coin['OPEN']['DATA']),
                'MAX': min(coin['OPEN']['DATA']),
                'AVG': [mean(coin["OPEN"]["DATA"][(coin["STEP"] * i):(coin["STEP"] * (i + 1)) - 1]) for i in
                        range(coin['RANGE'])],
            },
            'CLOSE': {
                'DATA': coin['CLOSE']['DATA'],
                'COUNT': len(coin['CLOSE']['DATA']),
                'MIN': min(coin['CLOSE']['DATA']),
                'MAX': min(coin['CLOSE']['DATA']),
                'AVG': [mean(coin["CLOSE"]["DATA"][(coin["STEP"] * i):(coin["STEP"] * (i + 1)) - 1]) for i in
                        range(coin['RANGE'])],
            },
            'HIGH': {
                'DATA': coin['HIGH']['DATA'],
                'COUNT': len(coin['HIGH']['DATA']),
                'MIN': min(coin['HIGH']['DATA']),
                'MAX': min(coin['HIGH']['DATA']),
                'AVG': [mean(coin["HIGH"]["DATA"][(coin["STEP"] * i):(coin["STEP"] * (i + 1)) - 1]) for i in
                        range(coin['RANGE'])],
            },
            'LOW': {
                'DATA': coin['LOW']['DATA'],
                'COUNT': len(coin['LOW']['DATA']),
                'MIN': min(coin['LOW']['DATA']),
                'MAX': min(coin['LOW']['DATA']),
                'AVG': [mean(coin["LOW"]["DATA"][(coin["STEP"] * i):(coin["STEP"] * (i + 1)) - 1]) for i in
                        range(coin['RANGE'])],
            },
            'RANGE': int(count / coin['STEP']),
            'FIBONACCI': {
                "DATA": {
                    "ASC": [[(float(max(coin["HIGH"]["DATA"][(coin["STEP"] * j):(coin["STEP"] * (j + 1)) - 1]) -
                                    float(
                                        max(coin["HIGH"]["DATA"][(coin["STEP"] * j):(coin["STEP"] * (j + 1)) - 1]) -
                                        min(coin["LOW"]["DATA"][(coin["STEP"] * j):(coin["STEP"] * (j + 1)) - 1])) *
                                    float(i / 100)))
                             for i in self.FIBONACCI_VALUES] for j in range(coin["RANGE"])],
                    "DESC": [[(float(min(coin["LOW"]["DATA"][(coin["STEP"] * j):(coin["STEP"] * (j + 1)) - 1]) +
                                     float(max(coin["HIGH"]["DATA"][(coin["STEP"] * j):(coin["STEP"] * (j + 1)) - 1]) -
                                           min(coin["LOW"]["DATA"][(coin["STEP"] * j):(coin["STEP"] * (j + 1)) - 1])) *
                                     float(i / 100)))
                              for i in self.FIBONACCI_VALUES] for j in range(coin["RANGE"])],
                },
                "MAX": [(float(max(coin["HIGH"]["DATA"][(coin["STEP"] * j):(coin["STEP"] * (j + 1)) - 1])))
                        for j in range(coin["RANGE"])],
                "MIN": [(float(min(coin["LOW"]["DATA"][(coin["STEP"] * j):(coin["STEP"] * (j + 1)) - 1])))
                        for j in range(coin["RANGE"])],
                "HIGH_LOW_AVG": [(float((mean(coin["HIGH"]["DATA"][(coin["STEP"] * j):(coin["STEP"] * (j + 1)) - 1]) +
                                         mean(coin["LOW"]["DATA"][
                                              (coin["STEP"] * j):(coin["STEP"] * (j + 1)) - 1])) / 2))
                                 for j in range(coin["RANGE"])],
                "OPEN_CLOSE_AVG": [(float((mean(coin["OPEN"]["DATA"][(coin["STEP"] * j):(coin["STEP"] * (j + 1)) - 1]) +
                                           mean(coin["CLOSE"]["DATA"][
                                                (coin["STEP"] * j):(coin["STEP"] * (j + 1)) - 1])) / 2))
                                   for j in range(coin["RANGE"])],
                "START_DATE": [((datetime.fromtimestamp(
                    min(coin["DATES"]["DATA"][(coin["STEP"] * j):(coin["STEP"] * (j + 1)) - 1]) / 1000.0
                )).strftime('%Y-%m-%d %H:%M:%S.%f')) for j in range(coin["RANGE"])],
                "END_DATE": [((datetime.fromtimestamp(
                    max(coin["DATES"]["DATA"][(coin["STEP"] * j):(coin["STEP"] * (j + 1)) - 1]) / 1000.0
                )).strftime('%Y-%m-%d %H:%M:%S.%f')) for j in range(coin["RANGE"])],
            }
        })
        temp = {"CLOSE_FINISHED_ARRAY": coin["CLOSE"]["DATA"][:-1]}
        coin["TA"]['MACD'], coin["TA"]["MACD_SIGNAL"], coin["TA"]["MACD_HISTOGRAM"] = \
            ta.MACD(np.asarray(temp["CLOSE_FINISHED_ARRAY"]))
        coin.update({
            'FIBONACCI': {
                "COUNT": len(coin["FIBONACCI"]["MAX"])
            },
            "TA": {
                'MACD': {
                    'DATA': coin['TA']['MACD'].tolist(),
                    'COUNT': len(coin['TA']['MACD'].tolist()),
                    'MIN': np.nanmin(coin['TA']['MACD'].tolist()),
                    'MAX': np.nanmax(coin['TA']['MACD'].tolist()),
                    'PREV': coin["TA"]["MACD"].tolist()[-2],
                    'LAST': coin['TA']['MACD'].tolist()[-1],
                },
                'MACD_SIGNAL': {
                    'DATA': coin['TA']['MACD_SIGNAL'].tolist(),
                    'COUNT': len(coin['TA']['MACD_SIGNAL'].tolist()),
                    'MIN': np.nanmin(coin['TA']['MACD_SIGNAL'].tolist()),
                    'MAX': np.nanmax(coin['TA']['MACD_SIGNAL'].tolist()),
                    'PREV': coin["TA"]["MACD_SIGNAL"].tolist()[-2],
                    'LAST': coin['TA']['MACD_SIGNAL'].tolist()[-1],
                },
                'MACD_HISTOGRAM': {
                    'DATA': coin['TA']['MACD_HISTOGRAM'].tolist(),
                    'COUNT': len(coin['TA']['MACD_HISTOGRAM'].tolist()),
                    'MIN': np.nanmin(coin['TA']['MACD_HISTOGRAM'].tolist()),
                    'MAX': np.nanmax(coin['TA']['MACD_HISTOGRAM'].tolist()),
                    'PREV': coin["TA"]["MACD_HISTOGRAM"].tolist()[-2],
                    'LAST': coin['TA']['MACD_HISTOGRAM'].tolist()[-1],
                },
                'RSI': {
                    'DATA': ta.RSI(np.asarray(temp["CLOSE_FINISHED_ARRAY"])).tolist(),
                    'COUNT': len(ta.RSI(np.asarray(temp["CLOSE_FINISHED_ARRAY"])).tolist()),
                    'MIN': np.nanmin(ta.RSI(np.asarray(temp["CLOSE_FINISHED_ARRAY"])).tolist()),
                    'MAX': np.nanmax(ta.RSI(np.asarray(temp["CLOSE_FINISHED_ARRAY"])).tolist()),
                    'PREV': ta.RSI(np.asarray(temp["CLOSE_FINISHED_ARRAY"])).tolist()[-2],
                    'LAST': ta.RSI(np.asarray(temp["CLOSE_FINISHED_ARRAY"])).tolist()[-1],
                },
            }
        })
        coin["TA"]["MACD_CROSS_UP"] = coin["TA"]["MACD"]["LAST"] > coin["TA"]["MACD_SIGNAL"]["LAST"] and \
            coin["TA"]["MACD"]["PREV"] < coin["TA"]["MACD_SIGNAL"]["PREV"]
        coin["TA"]["MACD_CROSS_DOWN"] = coin["TA"]["MACD"]["LAST"] < coin["TA"]["MACD_SIGNAL"]["LAST"] and \
            coin["TA"]["MACD"]["PREV"] > coin["TA"]["MACD_SIGNAL"]["PREV"]
        return coin
