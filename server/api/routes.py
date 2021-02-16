# server/api/routes.py
from server.api.views import (
    DocumentView,
    GameView,
    UserView,
    ResultView,
    RoundView,
    QuestionView,
    TopView
)


def setup_routes(app):
    app.router.add_view('/docs/{name}', DocumentView)
    app.router.add_view('/game', GameView)
    app.router.add_view('/users', UserView)
    app.router.add_view('/results/{game_id}', ResultView)
    app.router.add_view('/rounds', RoundView)
    app.router.add_view('/top', TopView)
    app.router.add_view('/question', QuestionView)
