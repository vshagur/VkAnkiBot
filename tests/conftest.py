import pytest

from server.api.main import get_app, get_db_config, set_db_client


@pytest.fixture()
def app():
    app = get_app()
    db_config = get_db_config()
    set_db_client(app, db_config)
    return app
