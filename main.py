import logging
from EXAMPLE import Trader
from datetime import datetime
import settings
import json
import os
import pandas as pd
from statistics import mean
import time
import pprint

fibonacci_values = [23.6, 38.2, 50.0, 61.8, 78.6]
# [(float(coinInfo["fibonacci"]["max"]) - float(coinInfo["fibonacci"]["max"]-coinInfo["fibonacci"]["min"]) * float(i/100) ) for i in fibonacci_values]

firstExchange = []
TOTALASSETS = 4800
BUYCOINSCOUNT = 3
logging.basicConfig(filename='std.log', filemode='w+', format='%(levelname)s - %(message)s')

DATA = []
with open("statistics.json","r+") as file:
    DATA = json.load(file)
    
COINS = DATA["mostCoins"]
STATISTICS = DATA["statistics"]


#def connectWallet():
    #return assets

#def buyCoin(BUYCOINSCOUNT, TOTALASSETS, DATA):

prices = Trader().getPrices(currency=[(i['coin']) for i in COINS])
#print(STATISTICS)
EXCHANGE = {}
totalUnitReceived = TOTALASSETS / len(COINS)

for i in list(prices.values()):
    tmp = float(totalUnitReceived) / float(i["price"])
    
    firstExchange.append(
        {
            "symbol":i["symbol"],
            "total":tmp,
            "price":float(i["price"]),
            "value":float(tmp*float(i["price"])), 
            "fibonacci_min":float(i["price"]),
            "fibonacci_max":float(i["price"]),
            "fibonacci":[(float(i["price"])*(j/100)) for j in fibonacci_values],
            "buy_point":float(i["price"])*1,
            "sell_point":float(i["price"])*1.5,
        }
    )
print(firstExchange)
sayac = 0
while(True):
    i=0
    currencies = []
    aa = {}        
    newPrices = Trader().getPrices(currency=[(i['coin']) for i in COINS])
    coin_stats = [(k) for k in STATISTICS if k["symbol"] in [(j["symbol"]) for j in firstExchange]]
    
    for index in range(len(firstExchange)):
        order = firstExchange[index]
        stat = [(stat) for stat in coin_stats if stat["symbol"] == order["symbol"]][0]
        logging.warning("Durum: "+str(order["symbol"])) 
        logging.warning("Fibonacci 38\t"+str(order["fibonacci"][1]))
        logging.warning("Fibonacci 61\t"+str(order["fibonacci"][3]))
        logging.warning("Price\t"+str(float(newPrices[order["symbol"]]['price'])))
        logging.warning("Fibonacci Max\t"+str(order["fibonacci_max"]))
        logging.warning("Fibonacci Min\t"+str(order["fibonacci_min"]))
        logging.warning("Esik\t"+str(float(order["price"]*1.007)))
        logging.warning("38 > price\t"+ ("Evet" if order["fibonacci"][1] > float(newPrices[order["symbol"]]['price']) else "Hayir"))
        logging.warning("Max > price\t"+ ("Evet" if order["fibonacci_max"]>float(newPrices[order["symbol"]]['price']) else "Hayir"))
        logging.warning("Esik Kar < price\t"+ ("Evet" if float(order["price"]*1.007)<float(newPrices[order["symbol"]]['price']) else "Hayir"))
        logging.warning("Total = 0\t"+ ("Evet" if ( order["total"]==0 ) else "Hayir"))
        logging.warning("Buy > Price\t"+ ("Evet" if order["buy_point"]>float(newPrices[order["symbol"]]['price']) else "Hayir"))
        logging.warning(" ")
        logging.warning(" ")
        if order["fibonacci"][1] > float(newPrices[order["symbol"]]['price']) and order["fibonacci_max"]>float(newPrices[order["symbol"]]['price']) and float(order["price"]*1.007)<float(newPrices[order["symbol"]]['price']):
            firstExchange[index] = {
                "symbol":order['symbol'], 
                "total":0, 
                "price":float(newPrices[order["symbol"]]['price']), 
                "value":str(float(newPrices[order["symbol"]]["price"])*float(order["total"])),
                "fibonacci_min":0,
                "fibonacci_max":0,
                "fibonacci":[((float(newPrices[order["symbol"]]['price'])) * float(j/100)) for j in fibonacci_values],
                "buy_point":order["fibonacci"][3],
                "sell_point":order["fibonacci"][1],
            }
            logging.warning("satti:"+str(firstExchange[index]))
            pprint.pprint(firstExchange[index])
        else:
            if order['total'] == 0 and order["buy_point"]>float(newPrices[order["symbol"]]['price']):
                firstExchange[index] = {
                    "symbol":order['symbol'], 
                    "total":float(firstExchange[index]['value'])/float(newPrices[order["symbol"]]['price']), 
                    "price":float(newPrices[order["symbol"]]['price']), 
                    "value":firstExchange[index]['value'],
                    "fibonacci_min":float(newPrices[order["symbol"]]['price']),
                    "fibonacci_max":float(newPrices[order["symbol"]]['price']),
                    "fibonacci":[((float(newPrices[order["symbol"]]['price'])) * float(j/100)) for j in fibonacci_values],
                    "buy_point":float(newPrices[order["symbol"]]['price'])*1,
                    "sell_point":float(newPrices[order["symbol"]]['price'])*1.5,
                }
                logging.warning("Aldi:"+str(firstExchange[index]))
                pprint.pprint(firstExchange[index])
            else:
                fibonacci_coin_max = order["fibonacci_max"] if (order["fibonacci_max"]>float(newPrices[order["symbol"]]["price"])) else float(newPrices[order["symbol"]]["price"])
                fibonacci_coin_points = [(float(fibonacci_coin_max) - float(fibonacci_coin_max-order["fibonacci_min"]) * float(j/100) ) for j in fibonacci_values]
                firstExchange[index] = {
                    "symbol":order['symbol'], 
                    "total":order['total'],
                    "price":order["price"],
                    "value":order["value"],
                    "fibonacci_min":order["fibonacci_min"],
                    "fibonacci_max": fibonacci_coin_max,
                    "fibonacci": fibonacci_coin_points,
                    "buy_point":fibonacci_coin_points[3],
                    "sell_point":fibonacci_coin_points[1]
                }
    if sayac < 2:
        pprint.pprint(firstExchange)
        sayac = sayac+1
    time.sleep(0.5)








k=0
def karar(step=15):
    coins = Trader().getPrices("USDT")
    coins_statistics = {"statistics":[]}
    most_coins = []
    #coins = str(os.getenv('CURRENCIES')).split(',')
    for coin in coins:
        timeData = Trader().getTimeData(currency=coin, minute=1)
        coinInfo = timeData["volume"] 
        coinInfo["high"] = {"min":min(timeData["high"]) ,"max":max(timeData["high"]),"avg":[]}
        coinInfo["low"] = {"min":min(timeData["low"]), "max":max(timeData["low"]),"avg":[]}
        coinInfo["open"] = {"min":min(timeData["open"]) ,"max":max(timeData["open"]),"avg":[]}
        coinInfo["close"] = {"min":min(timeData["open"]) ,"max":max(timeData["open"]),"avg":[]}
        coinInfo["fibonacci"] = {"asc":[],"desc":[],"values":[],"min":coinInfo["low"]["min"],"max":coinInfo["high"]["max"]}
        coinInfo["fibonacci"]["asc"] = [(float(coinInfo["fibonacci"]["max"]) - float(coinInfo["fibonacci"]["max"]-coinInfo["fibonacci"]["min"]) * float(i/100) ) for i in fibonacci_values]
        coinInfo["fibonacci"]["desc"] = [(float(coinInfo["fibonacci"]["min"]) + float(coinInfo["fibonacci"]["max"]-coinInfo["fibonacci"]["min"]) * float(i/100) ) for i in fibonacci_values]
        coinInfo["fibonacci"]["values"] = [(i) for i in fibonacci_values]
        coinInfo["dates"] = []
        coinInfo["avg"] = []
        count = len(timeData["dates"])
        index = int(count/step)
        coinInfo["artis_durum"] = 0
        for i in range(index):
            coinInfo["high"]["avg"].append(mean(timeData["high"][(step*(i)):(step*(i+1))-1]))
            coinInfo["low"]["avg"].append(mean(timeData["low"][(step*(i)):(step*(i+1))-1]))
            coinInfo["open"]["avg"].append(mean(timeData["open"][(step*(i)):(step*(i+1))-1]))
            coinInfo["close"]["avg"].append(mean(timeData["close"][(step*(i)):(step*(i+1))-1]))
            coinInfo["dates"].append(str(timeData["dates"][(step*(i))]+"-"+timeData["dates"][(step*(i+1))-1]))
            coinInfo["avg"].append((mean(timeData["high"][(step*(i)):(step*(i+1))-1])+
                    mean(timeData["low"][(step*(i)):(step*(i+1))-1]))/2)
            if coinInfo["avg"][i-1] != None:
                if coinInfo["avg"][i] / coinInfo["avg"][i-1] > 1:
                    coinInfo["artis_durum"] = coinInfo["artis_durum"]+1
                else:
                    coinInfo["artis_durum"] = coinInfo["artis_durum"]-1
        if(mean(coinInfo["avg"]) < float(coinInfo["lastPrice"])):
            coinInfo["alinma_durum"] = 'Evet'
        else:
            coinInfo["alinma_durum"] = 'Hayır'
        
        most_coins.append({"coin":coin,"artis":coinInfo["artis_durum"]})
        print(coin)
        print("Guncel Fiyat:",coinInfo["lastPrice"])
        print("Alinabilir:",coinInfo["alinma_durum"])
        print("Artis Durum:", coinInfo["artis_durum"])
        print("Savas Ortalama:",coinInfo["avg"][0])
        print("High Ortalama",coinInfo["high"]["avg"][0])
        print("Low Ortalama",coinInfo["low"]["avg"][0])
        print("Open Ortalama",coinInfo["open"]["avg"][0])
        print("Close Ortalama",coinInfo["close"]["avg"][0])
        print("Tarih",coinInfo["dates"][0])
        print("\n\n")
        coins_statistics["statistics"].append(coinInfo)
    most_coins = sorted(most_coins, key = lambda i: i["artis"])
    print(most_coins[len(most_coins)-5:])
    coins_statistics["mostCoins"] = most_coins[len(most_coins)-5:]
    with open('statistics.json', 'w') as outfile:
        json.dump(coins_statistics, outfile)
    
#karar()
    
'''

dates = []
open_data = []
high_data = []
low_data = []
close_data = []

for candle in aa:
    dates.append(datetime.fromtimestamp(candle[0] / 1000.0).strftime('%Y-%m-%d %H:%M:%S.%f'))
    open_data.append(candle[1])
    high_data.append(candle[2])
    low_data.append(candle[3])
    close_data.append(candle[4])
    
fig = go.Figure(data=[go.Candlestick(x=dates,
                       open=open_data, high=high_data,
                       low=low_data, close=close_data)])
fig.show()

'''
