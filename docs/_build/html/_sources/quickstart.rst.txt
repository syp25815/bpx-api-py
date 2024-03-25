Quickstart
===================

1. Install bpx SDK with:

.. code-block:: bash

   pip install bpx-api

2. Import :class:`bpx` and create the BpxClient using your **api key** and **secret key** from `Backpack settings`_:

.. _Backpack settings: https://backpack.exchange/settings/api-keys

.. code-block::

    from bpx import bpx
    api_key = "teq2s1yuev2Y8SZ7efCtQbPFzlpecHHm01I0N6IPdNI="
    secret_key = "9Z/KIv82cSg4y2fD4MY74ClR7S0O0J0AzN/7Aoe8BCo="
    bpx = bpx.BpxClient(api_key, secret_key)

3. With :class:`bpx` instance you can call methods:

.. code-block::

    deposits = bpx.deposits()
    balances = bpx.balances()

.. note::

    Public methods can be called using :class:`bpx\_pub` package without making class instances and API keys:

    .. code-block::

        from bpx import bpx_pub
        markets = bpx_pub.Markets()

Settings
============

You can also provide more options for :class:`bpx` class instance.

.. code-block::

    from bpx import bpx

    api_key = "teq2s1yuev2Y8SZ7efCtQbPFzlpecHHm01I0N6IPdNI="
    secret_key = "9Z/KIv82cSg4y2fD4MY74ClR7S0O0J0AzN/7Aoe8BCo="

    window = 10000
    proxies = {
    'http': 'http://10.10.1.10:3128'
    }
    bpx = bpx.BpxClient(api_key, secret_key, window, proxies)

