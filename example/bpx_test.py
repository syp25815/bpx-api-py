from bpx.bpx import *

if __name__ == '__main__':
    bpx = BpxClient()
    bpx.init('', '')

    print(bpx.depositAddress('Solana'))

    # print(bpx.balances())
    # print(bpx.deposits())
    #
    # print(bpx.withdrawals(10, 0))
    #
    # print(bpx.orderHistoryQuery('SOL_USDC', 10, 0))
    # print(bpx.fillHistoryQuery('SOL_USDC', 10, 0))
    # bpx.proxies = {'http': 'http://127.0.0', 'https': 'http://127.0.0.'}
    #
    # print(bpx.ExeOrder('SOL_USDC', 'Bid', 'Limit', 'IOC', '0.1', '116.35'))
    #
