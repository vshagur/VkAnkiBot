def format_top_players_message(users):
    text = 'Best players.\n'

    for num, user_data in enumerate(users, 1):
        success, win_games, total_games, user_id = user_data
        success = '{:.4%}'.format(success)
        text += f'\n{num}. {user_id}: success {success} in {total_games} games'

    return text


def format_game_aborted_messages(result):
    text = format_game_result_message(result)
    game_id = result.get('game_id')
    return f'Game "{game_id}" aborted.\n{text}'


def format_game_finished_messages(result):
    text = format_game_result_message(result)
    game_id = result.get('game_id')
    return f'Game "{game_id}" finished.\n{text}'


def format_game_result_message(result):
    users = result.get('users')
    score = result.get('score')

    text = f'Game results .'

    if users == [0, ]:
        text += '\nThere are no winners in the game.' \
                '\nThe number of participants in the game was less than 2 or all ' \
                'the answers were incorrect.'
    else:
        text += '\nThe winners of this game:\n'
        text += '\n'.join([f'{num}. {user}' for num, user in enumerate(users, 1)])
        text += f'\nPoints scored per game: {score}.'

    return text
