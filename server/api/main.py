# server/api/main.py
from aiohttp import web

from logger.logger import logger
from server.api.routes import setup_routes
from server.api.settings import config


def main():
    app = web.Application()
    setup_routes(app)
    app['config'] = config
    logger.debug(f'Load config: {config}')
    web.run_app(app)


if __name__ == '__main__':
    main()
