import aiohttp_jinja2, jinja2, pathlib

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


@aiohttp_jinja2.template('index.html')
async def index(request):
    return {}


async def message(request):
    data = await request.json()
    text = data.get('text', 'nothing')
    await request.app['ws_holder'].send(f'< Nobody >  {text}')
    return web.Response()


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    request.app['ws_holder'].add(ws)
    await request.app['ws_holder'].send(
        f"< {ws.headers['Sec-WebSocket-Accept']} >  HAS JOINED"
    )

    async for msg in ws:
        await request.app['ws_holder'].send(
            f"< {ws.headers['Sec-WebSocket-Accept']} >  {msg.data}"
        )

    request.app['ws_holder'].remove(ws)
    await request.app['ws_holder'].send(
        f"< {ws.headers['Sec-WebSocket-Accept']} >  HAS LEFT"
    )

    return ws


if __name__ == '__main__':
    app = web.Application()

    app.add_routes([web.get('/', index)])
    app.add_routes([web.get('/ws', websocket_handler)])
    app.add_routes([web.post('/message', message)])

    BASE_DIR = pathlib.Path(__file__).parent
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(BASE_DIR / 'templates')
    )

    app['ws_holder'] = WebsocketsHolder()

    web.run_app(app)
