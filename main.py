# This is a sample Python script.
import json
import pprint
import time
import logging

import Markets.settings
import os
from Markets.binance import Binance

DATA = []
STATISTICS = []
logging.basicConfig(filename='std.log', filemode='w+', format='%(levelname)s - %(message)s')


def statisticsCoins():
    binance = Binance()
    coins = str(os.getenv('CURRENCIES')).split(',')
    statistics_dict = {}
    for index in range(len(coins)):
        statistics_dict.update({coins[index]: binance.getTimeData(currency=coins[index], minute=1, step=15)})
        print(coins[index])
    with open('statistics.json', 'a+') as file:
        json.dump(statistics_dict, file)


def buyCoins():
    binance = Binance()

    with open("statistics.json", "r+") as file:
        JsonFile = json.load(file)

    print(JsonFile)
    coins = [coin for coin in JsonFile]
    prices = binance.getPrices(currency=coins)
    print(prices)

    totalUnitReceived = float(os.getenv('TOTALASSET')) / len(JsonFile)
    firstExchange = []
    print(prices)
    for coin, price in prices.items():
        tmp = float(totalUnitReceived) / float(price)
        firstExchange.append(
            {
                "symbol": coin,
                "total": tmp,
                "price": float(price),
                "value": float(tmp * float(price)),
                "fibonacci_min": float(price),
                "fibonacci_max": float(price),
                "fibonacci": [(float(price) * (j / 100)) for j in Binance.FIBONACCI_VALUES],
                "buy_point": float(price) * 1,
                "sell_point": float(price) * 1.5,
                "order_date": time.time(),
            }
        )
    with open('first-exchange.json', 'a+') as file:
        json.dump(firstExchange, file)


def checkCoins(filename='first-exchange.json'):
    binance = Binance()
    with open(filename, 'r+') as file:
        firstExchange = json.load(file)
        while True:
            newPrices = binance.getPrices(currency=[(i['symbol']) for i in firstExchange])
            for index in range(len(firstExchange)):
                order = firstExchange[index]
                fibonacci_coin_max = order["fibonacci_max"] \
                    if (order["fibonacci_max"] > float(newPrices[order["symbol"]]) and
                        order["fibonacci_max"] != 0) \
                    else float(newPrices[order["symbol"]])
                fibonacci_coin_min = order["fibonacci_min"] \
                    if (order["fibonacci_min"] < float(newPrices[order["symbol"]]) and
                        order["fibonacci_min"] != 0) \
                    else float(newPrices[order["symbol"]])
                fibonacci_coin_points = [
                    (float(fibonacci_coin_max) - float(fibonacci_coin_max - fibonacci_coin_min) * float(j / 100))
                    for j in Binance.FIBONACCI_VALUES
                ]

                logging.warning("Durum:\t" + str(order["symbol"]))
                logging.warning("Fibonacci 38\t" + str(order["fibonacci"][1]))
                logging.warning("Fibonacci 61\t" + str(order["fibonacci"][3]))
                logging.warning("Price\t\t" + str(float(newPrices[order["symbol"]])))
                logging.warning("Fibonacci Max\t" + str(order["fibonacci_max"]))
                logging.warning("Fibonacci Min\t" + str(order["fibonacci_min"]))
                logging.warning("Esik\t\t" + str(float(order["price"] * 1.007)))
                logging.warning("38 > Price\t" + (
                    "Evet" if order["fibonacci"][1] > float(newPrices[order["symbol"]]) else "Hayir"))
                logging.warning("Max > Price\t" + (
                    "Evet" if order["fibonacci_max"] > float(newPrices[order["symbol"]]) else "Hayir"))
                logging.warning("Esik < Price\t" + (
                    "Evet" if float(order["price"] * 1.007) < float(newPrices[order["symbol"]]) else "Hayir"))
                logging.warning("Total = 0\t" + ("Evet" if (order["total"] == 0) else "Hayir"))
                logging.warning("Buy > Price\t" + (
                    "Evet" if order["buy_point"] > float(newPrices[order["symbol"]]) else "Hayir"))
                logging.warning("Minute:\t" + str(divmod((int(time.time()) - int(order["order_date"])), 60)[0]))
                logging.warning(" ")
                logging.warning(" ")
                if order["fibonacci"][1] > float(newPrices[order["symbol"]]) and \
                        float(order["price"] * 1.007) < float(newPrices[order["symbol"]]):
                    # if order["fibonacci"][1] > float(newPrices[order["symbol"]])'''# and order[
                    # "fibonacci_max"]>float(newPrices[order["symbol"]]) ''' and float(order[
                    # "price"]*1.007)<float(newPrices[order["symbol"]]):
                    print('Satti')
                    firstExchange[index] = {
                        "symbol": order['symbol'],
                        "total": 0,
                        "price": float(newPrices[order["symbol"]]),
                        "value": str(float(newPrices[order["symbol"]]) * float(order["total"])),
                        "fibonacci_min": 0,
                        "fibonacci_max": 0,
                        "fibonacci": [(0*j) for j in Binance.FIBONACCI_VALUES],
                        "buy_point": float(newPrices[order["symbol"]]) / 1.007,
                        "sell_point": order["fibonacci"][1],
                        "order_date": time.time()
                    }
                    logging.warning("Satti:" + str(firstExchange[index]))
                    pprint.pprint(firstExchange[index])
                elif order['total'] == 0 and order["buy_point"] > float(newPrices[order["symbol"]]):
                    print('ALdi')
                    firstExchange[index] = {
                        "symbol": order['symbol'],
                        "total": float(firstExchange[index]['value']) / float(newPrices[order["symbol"]]),
                        "price": float(newPrices[order["symbol"]]),
                        "value": firstExchange[index]['value'],
                        "fibonacci_min": float(newPrices[order["symbol"]]),
                        "fibonacci_max": float(newPrices[order["symbol"]]),
                        "fibonacci": [(float(newPrices[order["symbol"]])) for j in Binance.FIBONACCI_VALUES],
                        "buy_point": float(newPrices[order["symbol"]]) / 1.007,
                        "sell_point": float(newPrices[order["symbol"]]) * 1.5,
                        "order_date": time.time()
                    }
                    logging.warning("Aldi:" + str(firstExchange[index]))
                    pprint.pprint(firstExchange[index])
                else:
                    firstExchange[index] = {
                        "symbol": order['symbol'],
                        "total": order['total'],
                        "price": order["price"],
                        "value": order["value"],
                        "fibonacci_min": fibonacci_coin_min,
                        "fibonacci_max": fibonacci_coin_max,
                        "fibonacci": fibonacci_coin_points,
                        "buy_point": order["price"] / 1.007,
                        "sell_point": fibonacci_coin_points[1],
                        "order_date": order["order_date"]
                    }



def print_hi():
    # Use a breakpoint in the code line below to debug your script.
    binance = Binance()
    try:
        pprint.pp(binance.getMarketDepth())
    except:
        print('e')


if __name__ == '__main__':
    checkCoins()
