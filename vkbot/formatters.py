def get_visible_name(user_id, first_name, last_name):
    if first_name or last_name:
        first_name = first_name or ''
        last_name = last_name or ''
        return ' '.join((first_name, last_name))
    else:
        return f'User {user_id}'


def format_top_players_message(users):
    text = 'Best players.'

    for num, user_data in enumerate(users, 1):
        success, win_games, total_games, user_id, first_name, last_name = user_data
        success = '{:.4%}'.format(success)
        visible_name = get_visible_name(user_id, first_name, last_name)
        text += f'\n{num}. {visible_name}: success {success} in {total_games} games'

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
    naming_dict = result.get('naming_dict')
    text = f'Game results .'

    if users == [0, ]:
        text += '\nThere are no winners in the game.' \
                '\nThe number of participants in the game was less than 2 or all ' \
                'the answers were incorrect.'
    else:
        text += '\nThe winners of this game:'

        for num, user_id in enumerate(users, 1):
            first_name = naming_dict[str(user_id)]['first_name']
            last_name = naming_dict[str(user_id)]['last_name']
            visible_name = get_visible_name(user_id, first_name, last_name)

            if len(users) == 1:
                num = sep = ''
            else:
                sep = '. '

            text += f'\n{num}{sep}{visible_name}'

        text += f'\nPoints scored per game: {score}.'

    return text


def format_new_game_message(data):
    vk_id = data.get('vk_id')
    game_id = data.get('game_id')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    visible_name = get_visible_name(vk_id, first_name, last_name)
    text = f'{visible_name} created a new game: {game_id}'

    return text
