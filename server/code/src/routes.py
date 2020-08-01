from aiohttp.web import get, post

from views import index, websocket_handler, message


def setup(app):
    app.add_routes([get('/', index)])
    app.add_routes([get('/ws', websocket_handler)])

    app.add_routes([post('/message', message)])
