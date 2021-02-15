def format_top_players_message(users):
    # TODO: add correct format
    # created vshagur@gmail.com, 2021-02-12
    text = 'Best players.\n'
    text += '\n'.join(f'{num}. {user}' for num, user in enumerate(users, 1))

    return text


def format_game_aborted_messages(result):
    text = format_game_result_message(result)
    return f'Game aborted.\n{text}'


def format_game_finished_messages(result):
    text = format_game_result_message(result)
    return f'Game finished.\n{text}'


def format_game_result_message(result):
    game_id = result.get('game_id')
    users = result.get('users')
    score = result.get('score')

    text = f'The result of the game is {game_id}.\n'
    text += '\n'.join([f'{num}. {user}' for num, user in enumerate(users, 1)])
    text += f'\nPoints scored per game: {score}.'

    return text
