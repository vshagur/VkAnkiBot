# server/api/routes.py
from views import index, docs


def setup_routes(app):
    app.router.add_get('/', index)
    app.router.add_get('/docs/{name}', docs)
