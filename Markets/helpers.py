import binance.enums


def minuteIntervalSwitch(minute):
    switch = {
        1: binance.enums.KLINE_INTERVAL_1MINUTE,
        3: binance.enums.KLINE_INTERVAL_3MINUTE,
        5: binance.enums.KLINE_INTERVAL_5MINUTE,
        15: binance.enums.KLINE_INTERVAL_15MINUTE,
        30: binance.enums.KLINE_INTERVAL_30MINUTE,
        60: binance.enums.KLINE_INTERVAL_1HOUR,
        120: binance.enums.KLINE_INTERVAL_2HOUR,
        240: binance.enums.KLINE_INTERVAL_4HOUR,
        360: binance.enums.KLINE_INTERVAL_6HOUR,
        480: binance.enums.KLINE_INTERVAL_8HOUR,
        720: binance.enums.KLINE_INTERVAL_12HOUR,
        1440: binance.enums.KLINE_INTERVAL_1DAY,
    }
    return switch.get(minute, lambda: binance.enums.KLINE_INTERVAL_15MINUTE)
