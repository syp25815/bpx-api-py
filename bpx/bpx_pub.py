import requests

BP_BASE_URL = ' https://api.backpack.exchange/'


# Markets

def Assets():
    return requests.get(url=f'{BP_BASE_URL}api/v1/assets').json()


def Markets():
    return requests.get(url=f'{BP_BASE_URL}api/v1/markets').json()


def Ticker(symbol: str):
    return requests.get(url=f'{BP_BASE_URL}api/v1/ticker?symbol={symbol}').json()


def Depth(symbol: str):
    return requests.get(url=f'{BP_BASE_URL}api/v1/depth?symbol={symbol}').json()


def KLines(symbol: str, interval: str, startTime: int = 0, endTime: int = 0):
    url = f'{BP_BASE_URL}api/v1/klines?symbol={symbol}&interval={interval}'

    if startTime > 0:
        url = f'{url}&startTime={startTime}'
    if endTime > 0:
        url = f'{url}&endTime={endTime}'

    return requests.get(url).json()


# System
def Status():
    return requests.get(url=f'{BP_BASE_URL}api/v1/status').json()


def Ping():
    return requests.get(url=f'{BP_BASE_URL}api/v1/ping').text


def Time():
    return requests.get(url=f'{BP_BASE_URL}api/v1/time').text


# Trades
def recentTrades(symbol: str, limit: int = 100):
    return requests.get(url=f'{BP_BASE_URL}api/v1/trades?symbol={symbol}&limit={limit}').json()


def historyTrades(symbol: str, limit: int = 100, offset: int = 0):
    return requests.get(url=f'{BP_BASE_URL}api/v1/trades/history?symbol={symbol}&limit={limit}&offset={offset}').json()


if __name__ == '__main__':
    # print(Assets())
    print(Markets())
    # print(Ticker('SOL_USDC'))
    # print(Depth('SOL_USDC'))
    # print(KLines('SOL_USDC', '1m'))
    # print(Status())
    # print(Ping())
    # print(Time())
    # print(recentTrades('SOL_USDC', 10))
    # print(historyTrades('SOL_USDC', 10))
    pass
