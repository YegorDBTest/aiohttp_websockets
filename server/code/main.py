from aiohttp import web


data = {
    'ws': None,
}




async def hello(request):
    return web.Response(text=str(data['ws']))


async def websocket_handler(request):

    data['ws'] = web.WebSocketResponse()
    await data['ws'].prepare(request)

    async for msg in data['ws']:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await data['ws'].close()
            else:
                await data['ws'].send_str(msg.data + '/answer')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  data['ws'].exception())

    print('websocket connection closed')

    return data['ws']


if __name__ == '__main__':
    app = web.Application()
    app.add_routes([web.get('/', hello)])
    app.add_routes([web.get('/ws', websocket_handler)])

    web.run_app(app)
