# server/api/routes.py
from views import (
    docs,
    add_user,
    add_game,
    update_game_info,
    get_top_players,
    get_game_result,
    get_question,
    add_round,
)


def setup_routes(app):
    app.router.add_get('/docs/{name}', docs)
    app.router.add_get('/results/{game_id}', get_game_result)
    app.router.add_post('/users', add_user)
    app.router.add_post('/rounds', add_round)
    app.router.add_post('/game', add_game)
    app.router.add_put('/game', update_game_info)
    app.router.add_get('/top', get_top_players)
    app.router.add_get('/question', get_question)
