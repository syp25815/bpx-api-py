from bpx.bpx import *

if __name__ == '__main__':
    bpx = BpxClient()

    bpx.init("teq2s1yuev2Y8SZ7efCtQbPFzlpecHHm01I0N6IPdNI=", "9Z/KIv82cSg4y2fD4MY74ClR7S0O0J0AzN/7Aoe8BCo=")

    # print(bpx.depositAddress('Solana'))
    #
    # print(bpx.balances())
    # print(bpx.deposits())
    # #
    # print(bpx.withdrawals(10, 0))

    bpx.debug = True

    # print(bpx.withdrawal("", "USDC", "Solana", "600"))

    # print(bpx.orderQuery('SOL_USDC', '111948072781414400'))
    # print(bpx.ordersQuery(''))

    # print(bpx.orderCancel('SOL_USDC','111947854837907456'))
    # print(bpx.ordersCancel('SOL_USDC'))

    #
    # print(bpx.orderHistoryQuery('SOL_USDC', 10, 0))
    # print(bpx.fillHistoryQuery('SOL_USDC', 10, 0))
    # bpx.proxies = {'http': 'http://127.0.0', 'https': 'http://127.0.0.'}
    #
    # print(bpx.ExeOrder('SOL_USDC', 'Bid', 'Limit', 'IOC', '0.1', '116.35'))
    # print(bpx.ExeOrder('SOL_USDC', 'Bid', 'Limit', '', '1', '13'))
    #
