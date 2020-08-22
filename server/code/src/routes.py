from pathlib import Path

from aiohttp.web import get, post, static

from views import index, websocket_handler, message


def setup(app):
    app.add_routes([get('/', index)])
    app.add_routes([get('/ws', websocket_handler)])

    app.add_routes([post('/message', message)])

    app.add_routes([static('/static', Path(__file__).parent / 'static')])
