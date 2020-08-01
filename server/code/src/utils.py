class WebsocketsHolder:
    def __init__(self):
        self._items = {}

    def __iter__(self):
        return iter(self._items.values())

    def add(self, ws):
        self._items[ws.headers['Sec-WebSocket-Accept']] = ws

    def remove(self, ws):
        del self._items[ws.headers['Sec-WebSocket-Accept']]

    async def send(self, message):
        for ws in self:
            await ws.send_str(message)
