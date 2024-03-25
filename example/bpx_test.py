from bpx.bpx import *

if __name__ == '__main__':
    proxies = {'http': 'http://127.0.0', 'https': 'http://127.0.0.'}
    bpx = BpxClient("mGdcu6JpPtErk/5OrAUU61RKmPqMLaI62fyxYsIMqkM=", "3+OeXRKtDCBtU3w9/gxKm/2RfWhkYfYDx73M/a+deJ0=")


    # print(bpx.depositAddress('Solana'))
    #
    # print(bpx.balances())

    print(bpx.deposits())
    # #
    # print(bpx.get_withdrawals(10, 0))

    bpx.debug = True

    # print(bpx.withdrawal("", "USDC", "Solana", "600"))

    # print(bpx.orderQuery('SOL_USDC', '111948072781414400'))
    # print(bpx.ordersQuery(''))

    # print(bpx.orderCancel('SOL_USDC','111947854837907456'))
    # print(bpx.ordersCancel('SOL_USDC'))

    #
    # print(bpx.orderHistoryQuery('SOL_USDC', 10, 0))
    # print(bpx.fillHistoryQuery('SOL_USDC', 100, 0, 0, 1000000000000000000))
    #
    # print(bpx.ExeOrder('SOL_USDC', 'Bid', 'Limit', 'IOC', '0.1', '116.35'))
    # print(bpx.ExeOrder('SOL_USDC', 'Bid', 'Limit', '', '1', '13'))

