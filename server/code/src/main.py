from aiohttp.web import Application, run_app

from aiohttp_jinja2 import setup as jinja2_setup

from jinja2 import FileSystemLoader

from routes import setup as routes_setup
from settings import TEMPLATES_DIR
from utils import WebsocketsHolder


def start():
    app = Application()

    jinja2_setup(app, loader=FileSystemLoader(TEMPLATES_DIR))
    routes_setup(app)

    app['ws_holder'] = WebsocketsHolder()

    run_app(app)


if __name__ == '__main__':
    start()
