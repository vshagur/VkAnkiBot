# server/api/main.py
import os

from aiohttp import web
from logger.logger import logger
from server.api.routes import setup_routes
from server.api.settings import config
from time import sleep
from db.db_client import DbClient
from aiohttp_apispec import setup_aiohttp_apispec
from aiohttp_swagger import setup_swagger


def get_db_config():
    return {
        'db_user': os.getenv('POSTGRES_USER'),
        'db_password': os.getenv('POSTGRES_PASSWORD'),
        'db_name': os.getenv('POSTGRES_DB'),
        'db_host': os.getenv('POSTGRES_HOST'),
    }


def get_app():
    app = web.Application()
    setup_routes(app)
    app['config'] = config
    logger.debug(f'Load config: {config}')
    setup_aiohttp_apispec(app)

    async def swagger(app):
        setup_swagger(
            app=app, swagger_url='/api/doc', swagger_info=app['swagger_dict']
        )

    app.on_startup.append(swagger)

    return app


def set_db_client(app, db_config):
    db_client = DbClient(db_config)
    db_client.setup(app)


def main():
    app = get_app()
    db_config = get_db_config()
    set_db_client(app, db_config)
    # TODO: узнать, как дождаться инициализаци базы данных при первом запуске
    # чтобы не возникало ошибок, использование sleep временное решение
    # created vshagur@gmail.com, 2021-02-19
    sleep(5)
    web.run_app(app)


if __name__ == '__main__':
    main()
