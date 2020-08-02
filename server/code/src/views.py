from aiohttp.web import Response, WebSocketResponse

from aiohttp_jinja2 import template


@template('index.html')
async def index(request):
    return {}


async def message(request):
    data = await request.json()
    text = data.get('text', 'nothing')
    await request.app['ws_holder'].send('Nobody', text)
    return Response()


async def websocket_handler(request):
    ws = WebSocketResponse()
    await ws.prepare(request)

    request.app['ws_holder'].add(ws)
    await request.app['ws_holder'].send(
        'staff',
        f"{ws.headers['Sec-WebSocket-Accept']}  HAS JOINED",
    )

    async for msg in ws:
        await request.app['ws_holder'].send(ws.headers['Sec-WebSocket-Accept'], msg.data)

    request.app['ws_holder'].remove(ws)
    await request.app['ws_holder'].send(
        'staff',
        f"{ws.headers['Sec-WebSocket-Accept']}  HAS LEFT",
    )

    return ws
