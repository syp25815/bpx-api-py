import rel
import websocket
from bpx.bpx import *


def on_message(ws, message):
    print('Received message: {}'.format(message))
    # data = json.loads(message)
    #
    # print(f'流事件：{data["stream"]} 流数据: {data["data"]["e"]} 代币: {data["data"]["s"]}')
    # # print(message['stream'])
    # print(message)


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):
    print("Opened connection")


if __name__ == '__main__':
    bpx = BpxClient()

    bpx.init("", "")

    print(bpx.depositAddress('Solana'))

    # # websocket.WebSocket
    ws = websocket.WebSocketApp("wss://ws.backpack.exchange",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    #
    ws.run_forever(dispatcher=rel,
                   reconnect=5)

    params = {
        "method": "SUBSCRIBE",
        "params": ["account.orderUpdate"],
        "signature": bpx.ws_sign('subscribe'),

    }

    ws.send(json.dumps(params))
    #
    #
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()
