from bpx.bpx_pub import *

if __name__ == '__main__':
    print(Assets())
    print(Markets())
    print(Ticker('SOL_USDC'))
    print(Depth('SOL_USDC'))
    print(KLines('SOL_USDC', '1m'))
    print(Status())
    print(Ping())
    print(Time())
    print(recentTrades('SOL_USDC', 10))
    print(historyTrades('SOL_USDC', 10))
