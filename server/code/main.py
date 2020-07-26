from aiohttp import web


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


async def index(request):
    data = []
    for ws in request.app['ws_holder']:
        data.append(str(ws.headers['Sec-WebSocket-Accept']))
    return web.Response(text='\n'.join(data))


async def message(request):
    text = request.query.get('text', 'nothing')
    await request.app['ws_holder'].send(text)
    return web.Response(text='Sended')


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    request.app['ws_holder'].add(ws)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str(msg.data + '/answer')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    request.app['ws_holder'].remove(ws)
    return ws


if __name__ == '__main__':
    app = web.Application()

    app.add_routes([web.get('/', index)])
    app.add_routes([web.get('/message', message)])
    app.add_routes([web.get('/ws', websocket_handler)])

    app['ws_holder'] = WebsocketsHolder()

    web.run_app(app)
