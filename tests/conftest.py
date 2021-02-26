import pytest
from gino import GinoEngine
from server.api.main import get_app, get_db_config, set_db_client
import functools


@pytest.fixture()
def app():
    app = get_app()
    db_config = get_db_config()
    set_db_client(app, db_config)
    return app


@pytest.fixture
async def api_test_client(test_client, app):
    client = await test_client(app)
    yield client

# @pytest.fixture(autouse=True)
# async def db_transaction(api_test_client):
#
#     db = api_test_client.app["db_client"].db
#     real_acquire = GinoEngine.acquire
#
#     async with db.acquire() as conn:
#
#         class _AcquireContext:
#             __slots__ = ["_acquire", "_conn"]
#
#             def __init__(self, acquire):
#                 self._acquire = acquire
#
#             async def __aenter__(self):
#                 return conn
#
#             async def __aexit__(self, exc_type, exc_val, exc_tb):
#                 pass
#
#             def __await__(self):
#                 return conn
#
#         def acquire(
#             self, *, timeout=None, reuse=False, lazy=False, reusable=True
#         ):
#             return _AcquireContext(
#                 functools.partial(self._acquire, timeout, reuse, lazy, reusable)
#             )
#
#         GinoEngine.acquire = acquire
#         transaction = await conn.transaction()
#         yield
#         await transaction.rollback()
#         GinoEngine.acquire = real_acquire
