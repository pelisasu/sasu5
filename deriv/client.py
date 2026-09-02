import json
import time
import websocket

WS_URL = "wss://ws.binaryws.com/websockets/v3"

class DerivClient:
    def __init__(self, timeout=20):
        self.timeout = timeout

    def request(self, payload):
        ws = websocket.create_connection(WS_URL, timeout=self.timeout)
        try:
            ws.send(json.dumps(payload))
            deadline = time.time() + self.timeout
            while time.time() < deadline:
                raw = ws.recv()
                data = json.loads(raw)
                if data.get("error"):
                    raise RuntimeError(data["error"].get("message", "Deriv API error"))
                return data
            raise TimeoutError("Deriv response timeout")
        finally:
            ws.close()

    def active_symbols(self):
        return self.request({
            "active_symbols": "brief",
            "product_type": "basic"
        }).get("active_symbols", [])

    def ticks_history(self, symbol, count=500, granularity=60):
        return self.request({
            "ticks_history": symbol,
            "end": "latest",
            "count": count,
            "style": "candles",
            "granularity": granularity,
            "adjust_start_time": 1,
            "subscribe": 0
        })

    def latest_tick(self, symbol):
        return self.request({"ticks": symbol})
