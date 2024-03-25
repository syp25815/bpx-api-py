import base64
import json
import time
import requests
from cryptography.hazmat.primitives.asymmetric import ed25519


class BpxClient:
    """

        :param api_key:  Base64 encoded verifying key of the ED25519 keypair.
        :type api_key: :class:`str`
        :param api_secret: private key of the ED25519 keypair that corresponds to the public key
        :type api_secret: :class:`str`
        :param window: Time window in milliseconds that the request is valid for, default is ``5000`` and maximum is ``60000``
        :type window: :class:`int64`, optional
        :param proxies: Proxy that will be used for requests. More details about format on `requests documentation`_.
        :type proxies: :class:`dict`, optional
        .. _requests documentation: https://requests.readthedocs.io/en/latest/user/advanced/#proxies

    """
    _URL = 'https://api.backpack.exchange/'
    debug = False
    debugTs = 0

    def __init__(self, api_key: str, api_secret: str, window: int = 5000, proxies: dict = None):
        self.api_key = api_key
        self.private_key = ed25519.Ed25519PrivateKey.from_private_bytes(
            base64.b64decode(api_secret)
        )
        self.proxies = proxies
        self.window = window

    def _handle_bpx_request(self, url, headers, params=None, r_type='GET'):
        if r_type == 'GET':
            response = requests.get(url=url, proxies=self.proxies, headers=headers, params=params)
        elif r_type == 'POST':
            response = requests.post(url=url, proxies=self.proxies, headers=headers, data=json.dumps(params))
        else:
            response = requests.delete(url=url, proxies=self.proxies, headers=headers, data=json.dumps(params))
        try:
            return response.json()
        except json.JSONDecodeError:
            return response.text

    # capital
    def balances(self):
        """
        :return: Account balances and the state of the balances (locked or available).
        :rtype: :class:`dict`
        """
        return self._handle_bpx_request(url=f'{self._URL}api/v1/capital',
                                        headers=self._sign('balanceQuery'))

    def deposits(self, limit: int = 100, offset: int = 0):
        """
        :param limit: Maximum number to return. Default ``100``, maximum ``1000``.
        :type limit: :class:`int64`
        :param offset: The offset of retrieving data. Default ``0``.
        :type offset: :class:`int64`
        :return: Deposit history.
        :rtype: :class:`dict`
        """
        params = {
            'limit': limit,
            'offset': offset,
        }
        return self._handle_bpx_request(url=f'{self._URL}wapi/v1/capital/deposits',
                                        headers=self._sign('depositQueryAll', params),
                                        params=params)

    def depositAddress(self, chain: str):
        """

        :param chain: Blockchain symbol to get a deposit address for.
        :type chain: :class:`str`
        :return: User specific deposit address if the user were to deposit on the specified blockchain.
        :rtype: :class:`dict`
        """
        params = {'blockchain': chain}
        return self._handle_bpx_request(url=f'{self._URL}wapi/v1/capital/deposit/address',
                                        headers=self._sign('depositAddressQuery', params),
                                        params=params)

    # set withdrawal address:
    # https://backpack.exchange/settings/withdrawal-addresses?twoFactorWithdrawalAddress=true
    def get_withdrawals(self, limit: int = 100, offset: int = 0):
        """

        :param limit: Maximum number to return. Default ``100``, maximum ``1000``.
        :type limit: :class:`int64`
        :param offset: Offset. Default ``0``.
        :type offset: :class:`int64`
        :return: Withdrawal history.
        :rtype: :class:`dict`
        """
        params = {'limit': limit, 'offset': offset}
        return self._handle_bpx_request(url=f'{self._URL}wapi/v1/capital/withdrawals',
                                        headers=self._sign('withdrawalQueryAll', params),
                                        params=params)

    def withdrawal(self, address: str, symbol: str, blockchain: str, quantity: str, twoFactorToken: str = None):
        """

        :param address: Address to withdraw to.
        :type address: :class:`str`
        :param symbol: Blockchain to withdraw on.
        :type symbol: :class:`str`
        :param blockchain: Quantity to withdraw.
        :type blockchain: :class:`str`
        :param quantity: Symbol of the asset to withdraw.
        :type quantity: :class:`str`
        :param twoFactorToken: Issued two factor token.
        :type twoFactorToken: :class:`str`
        :return: Requests a withdrawal from the exchange.
        :rtype: :class:`dict`

        .. note::

            The twoFactorToken field is required if the withdrawal address is not an address that is configured in the address book to not require 2FA. These addresses can be configured `here`_.

            .. _here: https://backpack.exchange/settings/withdrawal-addresses?twoFactorWithdrawalAddress=true

        """
        params = {
            'address': address,
            'blockchain': blockchain,
            'quantity': quantity,
            'symbol': symbol,
        }
        if twoFactorToken:
            params['twoFactorToken'] = twoFactorToken
        return self._handle_bpx_request(url=f'{self._URL}wapi/v1/capital/withdrawals',
                                        headers=self._sign('withdraw', params),
                                        params=params,
                                        r_type='POST')

    # history

    def orderHistoryQuery(self, symbol: str, limit: int = 100, offset: int = 0):
        """

        :param symbol: Filter to the given symbol.
        :type symbol: :class:`str`
        :param limit: Maximum number to return. Default ``100``, maximum ``1000``.
        :type limit: :class:`int64`
        :param offset: Offset. Default ``0``.
        :type offset: :class:`int64`
        :return: Order history for the user. This includes orders that have been filled and are no longer on the book. It may include orders that are on the book, but the ``/orders`` endpoint contains more up to date data.
        :rtype: :class:`dict`
        """
        params = {'symbol': symbol, 'limit': limit, 'offset': offset}
        return self._handle_bpx_request(url=f'{self._URL}wapi/v1/history/orders', params=params,
                                        headers=self._sign('orderHistoryQueryAll', params))

    def fillHistoryQuery(self, symbol: str, limit: int = 100, offset: int = 0, __from: int = None, to: int = None):
        """

        :param symbol: Filter to the given symbol.
        :type symbol: :class:`str`
        :param limit: Offset. Default ``0``.
        :type limit: :class:`int64`
        :param offset: Maximum number to return. Default ``100``, maximum ``1000``.
        :type offset: :class:`int64`
        :param __from: Filter to minimum time (milliseconds).
        :type __from: :class:`int64`, optional
        :param to: Filter to maximum time (milliseconds).
        :type to: :class:`int64`, optional
        :return: Historical fills, with optional filtering for a specific order or symbol.
        """
        params = {
            'from': __from,
            'symbol': symbol,
            'to': to,
            'limit': limit,
            'offset': offset,
        }

        return self._handle_bpx_request(url=f'{self._URL}wapi/v1/history/fills', params=params,
                                        headers=self._sign('fillHistoryQueryAll', params))

    # order

    def orderQuery(self, symbol: str, orderId: str = None, clientId: int = None):
        """

        :param symbol: Market symbol for the order.
        :type symbol: :class:`str`
        :param orderId: ID of the order.
        :type orderId: :class:`int64`
        :param clientId: Client ID of the order.
        :type clientId: :class:`int64`
        :return: open order from the order book. This only returns the order if it is resting on the order book (i.e. has not been completely filled, expired, or cancelled).
        :rtype: :class:`dict`

        .. note::

            One of ``orderId`` or ``clientId`` must be specified. If both are specified, then ``orderId`` takes precedence.

        """

        params = {'symbol': symbol}
        if orderId:
            params['orderId'] = orderId
        if clientId:
            params['clientId'] = clientId
        return self._handle_bpx_request(url=f'{self._URL}api/v1/order', params=params,
                                        headers=self._sign('orderQuery', params))

    def ExeOrder(self, symbol: str, side: str, orderType: str,
                 timeInForce: str, quantity: float, price: float, triggerPrice: float,
                 selfTradePrevention: str = "RejectBoth", quoteQuantity: float = None,

                 ):
        """

        :param symbol: The market for the order.
        :type symbol: :class:`str`
        :param side: Which side of the order book the order is on.
        :type side: :class:`str`
        :param orderType: The type of an order.
        :type orderType: :class:`str`
        :param timeInForce:
        :type timeInForce: :class:`str`
        :param quantity: The order quantity. Market orders must specify either a ``quantity`` or ``quoteQuantity``. All other order types must specify a ``quantity``.
        :type quantity: :class:`float`
        :param price: The order price if this is a limit order.
        :type price: :class:`float`
        :param triggerPrice: Trigger price if this is a conditional order.
        :type triggerPrice: :class:`float`
        :param selfTradePrevention: Self trade prevention describes what should happen if the order attempts to fill against another order from the same account or trade group.
        :type selfTradePrevention: :class:`str`
        :param quoteQuantity: The maximum amount of the quote asset to spend (Ask) or receive (Bid) for market orders. This is used for reverse market orders. The order book will execute a ``quantity`` as close as possible to the notional value of ``quote_quantity``.
        :type quoteQuantity: :class:`float`
        :return: Status of executed order.
        :rtype: :class:`dict`

        """

        params = {
            'symbol': symbol,
            'side': side,
            'orderType': orderType,
            'quantity': quantity,
            'price': price,
            'selfTradePrevention': selfTradePrevention,
        }
        if triggerPrice:
            params['triggerPrice'] = triggerPrice
        if quoteQuantity:
            params['quoteQuantity'] = quoteQuantity
        if len(timeInForce) < 1:
            params['postOnly'] = True
        else:
            params['timeInForce'] = timeInForce
        return self._handle_bpx_request(url=f'{self._URL}api/v1/order', params=params,
                                        headers=self._sign('orderExecute', params), r_type='POST')

    def orderCancel(self, symbol: str, orderId: str = None, clientId: int = None):
        """

        :param symbol: Market the order exists on.
        :type symbol: :class:`str`
        :param orderId: ID of the order.
        :type orderId: :class:`int64`
        :param clientId: Market the order exists on.
        :type clientId: :class:`int64`
        :return: Status of canceling the order.
        :rtype: :class:`dict`

        .. note::

            One of ``orderId`` or ``clientId`` must be specified. If both are specified, then ``orderId`` takes precedence.
`
        """

        params = {'symbol': symbol}
        if orderId:
            params['orderId'] = orderId
        if clientId:
            params['clientId'] = clientId
        return self._handle_bpx_request(url=f'{self._URL}api/v1/order', params=params,
                                        headers=self._sign('orderCancel', params), r_type='DELETE')

    def ordersQuery(self, symbol: str = None):
        """

        :param symbol: The symbol of the market for the orders.
        :type symbol: :class:`str`, optional
        :return: Retrieves all open orders. If a symbol is provided, only open orders for that market will be returned, otherwise all open orders are returned.
        :rtype: :class:`dict`
        """
        params = {}
        if len(symbol) > 0:
            params['symbol'] = symbol

        return self._handle_bpx_request(url=f'{self._URL}api/v1/orders', params=params,
                                        headers=self._sign('orderQueryAll', params))

    def orderCancelAll(self, symbol: str):
        """

        :param symbol: Market to cancel orders for.
        :type symbol: :class:`str`
        :return: Cancels all open orders on the specified market.
        :rtype: :class:`dict`
        """
        params = {'symbol': symbol}
        return self._handle_bpx_request(url=f'{self._URL}api/v1/orders', params=params,
                                        headers=self._sign('orderCancelAll', params), r_type='DELETE')

    def _sign(self, instruction: str, params=None):
        ts = int(time.time() * 1e3)
        encoded_signature = self._build_sign(instruction, ts, params)
        headers = {
            "X-API-Key": self.api_key,
            "X-Signature": encoded_signature,
            "X-Timestamp": str(ts),
            "X-Window": str(self.window),
            "Content-Type": "application/json; charset=utf-8",
        }
        return headers

    def _ws_sign(self, instruction: str, params=None):
        ts = int(time.time() * 1e3)
        encoded_signature = self._build_sign(instruction, ts, params)
        # 必须将ts、window转为字符串，不然报错： Parse error
        result = [self.api_key, encoded_signature, str(ts), str(self.window)]
        return result

    def _build_sign(self, instruction: str, ts: int, params=None):
        sign_str = f"instruction={instruction}" if instruction else ""
        if params is None:
            params = {}
        if 'postOnly' in params:
            params = params.copy()
            params['postOnly'] = str(params['postOnly']).lower()
        sorted_params = "&".join(
            f"{key}={value}" for key, value in sorted(params.items())
        )
        if sorted_params:
            sign_str += "&" + sorted_params
        if self.debug and self.debugTs > 0:
            ts = self.debugTs
        sign_str += f"&timestamp={ts}&window={self.window}"
        signature_bytes = self.private_key.sign(sign_str.encode())
        encoded_signature = base64.b64encode(signature_bytes).decode()
        if self.debug:
            print(f'Waiting Sign Str: {sign_str}')
            print(f"Signature: {encoded_signature}")
        return encoded_signature
