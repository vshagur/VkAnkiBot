import asyncio
import json

from keyboard import VkKeyboard, VkKeyboardColor, get_command_keyboard, get_quiz_keyboard
from logger import logger


class Command:
    """Base class for all commands"""

    @classmethod
    async def execute(cls, bot_logic, update_content):
        if cls.is_running(bot_logic, update_content):
            await cls.execute_if_game_in_progress(bot_logic, update_content)
        else:
            await cls.execute_if_wait_game(bot_logic, update_content)

    @classmethod
    async def execute_if_game_in_progress(cls, bot_logic, update_content):
        await asyncio.sleep(0)

    @classmethod
    async def execute_if_wait_game(cls, bot_logic, update_content):
        await asyncio.sleep(0)

    @classmethod
    def is_running(cls, bot_logic, update_content):
        return update_content.get('peer_id') in bot_logic.running_games

    @classmethod
    async def activate_timer(cls, bot_logic, game_id, round_id, from_id, peer_id,
                             random_id, user_id, timeout, command):
        payload = {
            'command': command,
            'game_id': game_id,
            'round_id': round_id,
            'user_id': user_id,
        }

        timer = {
            'object': {
                'peer_id': peer_id,
                'random_id': random_id,
                'from_id': from_id,
                'payload': json.dumps(payload),
                'date': timeout,
            },
            'type': 'message_new'
        }

        await asyncio.sleep(1)
        bot_logic.queue.put_nowait(timer)

    @classmethod
    async def send(cls, bot_logic, payload):
        url = bot_logic.url
        new_payload = payload.copy()
        new_payload.update(bot_logic.payload)

        async with bot_logic.session.post(url, data=new_payload) as resp:
            if resp.status == 200:
                content = await resp.json()
            else:
                logger.error(f'RESPONSE_CODE_NOT_200. URL: {url}. CODE: {resp.status}.')

    @classmethod
    async def send_command_keyboard(cls, bot_logic, peer_id, random_id):
        keyboard = get_command_keyboard()
        payload = {
            'keyboard': keyboard.get_keyboard(),
            'peer_id': peer_id,
            'random_id': random_id,
            'message': (
                'Choose an action:\n'
                '"Help" - get help about the game\n'
                '"Top Players" - Bring out the top 10 players\n'
                '"Start game" - create a new game'
            )
        }

        await cls.send(bot_logic, payload)


class Abort(Command):

    @classmethod
    async def execute_if_game_in_progress(cls, bot_logic, update_content):

        # parse data
        try:
            resp_payload = json.loads(update_content.get('payload'))
            resp_game_id = resp_payload.get('game_id')

            if resp_game_id is None:
                logger.error(f'Not_correct_game_id: {resp_game_id}')
                await asyncio.sleep(0)
                return

        except (TypeError, json.JSONDecodeError) as err:
            logger.error(err)
            await asyncio.sleep(0)
            return

        from_id = update_content['from_id']
        peer_id = update_content['peer_id']
        random_id = update_content['random_id']
        user_id = bot_logic.running_games[peer_id]['user_id']
        game_id = bot_logic.running_games[peer_id]['game_id']

        # check that the user can stop the game
        if user_id == from_id and resp_game_id == game_id:
            # update the data about the game in the database (the game is over)
            payload = {'status': 'done'}
            await bot_logic.api_client.update_game_info(game_id, payload)

            # get game result from db
            result = await bot_logic.api_client.get_result(game_id)

            # clear game data
            del bot_logic.running_games[peer_id]

            # send game report to user
            payload = {
                'peer_id': peer_id,
                'random_id': random_id,
                # TODO: format message
                # created vshagur@gmail.com, 2021-02-11
                'message': f'Game aborted. Results: {result}',
            }

            await cls.send(bot_logic, payload)

            # send command keyboard to user
            await cls.send_command_keyboard(bot_logic, peer_id, random_id)

        else:
            # send notification to user
            payload = {
                'peer_id': peer_id,
                'random_id': random_id,
                'message': 'Only the user who started the game can stop it.',
            }
            await cls.send(bot_logic, payload)


class Help(Command):

    @classmethod
    async def execute_if_wait_game(cls, bot_logic, update_content):
        # get help page from db
        data = await bot_logic.api_client.get_help()

        # send help page to user
        help_page = data.get('text')
        peer_id = update_content['peer_id']
        random_id = update_content['random_id']

        payload = {
            'peer_id': peer_id,
            'random_id': random_id,
            'message': help_page,
        }

        await cls.send(bot_logic, payload)

        # send command keyboard
        await cls.send_command_keyboard(bot_logic, peer_id, random_id)


class Start(Command):

    @classmethod
    async def execute_if_game_in_progress(cls, bot_logic, update_content):
        # TODO: добавить логику для запущеной игры
        # created vshagur@gmail.com, 2021-02-12
        await asyncio.sleep(0)

    @classmethod
    async def execute_if_wait_game(cls, bot_logic, update_content):
        # add new user to db
        # TODO: add getting full data about user by id
        # created vshagur@gmail.com, 2021-02-11
        from_id = update_content['from_id']
        peer_id = update_content['peer_id']
        random_id = update_content['random_id']
        await bot_logic.api_client.add_user(from_id)

        # send command keyboard to user
        await cls.send_command_keyboard(bot_logic, peer_id, random_id)


class Top(Command):

    @classmethod
    async def execute_if_game_in_progress(cls, bot_logic, update_content):
        await asyncio.sleep(0)

    @classmethod
    async def execute_if_wait_game(cls, bot_logic, update_content):
        # get report from db
        top_players = await bot_logic.api_client.get_top_players()

        # send report to user
        peer_id = update_content['peer_id']
        random_id = update_content['random_id']
        # TODO: add correct format
        # created vshagur@gmail.com, 2021-02-12
        users = top_players.get('users')
        report = '\n'.join(f'{num}. {user}' for num, user in enumerate(users, 1))

        payload = {
            'peer_id': peer_id,
            'random_id': random_id,
            'message': report,
        }

        await cls.send(bot_logic, payload)

        # send command keyboard to user
        await cls.send_command_keyboard(bot_logic, peer_id, random_id)


class NotExistCommand(Command):

    @classmethod
    async def execute_if_wait_game(cls, bot_logic, update_content):
        # send command keyboard to user
        peer_id = update_content['peer_id']
        random_id = update_content['random_id']
        await cls.send_command_keyboard(bot_logic, peer_id, random_id)


class New(Command):

    @classmethod
    async def execute_if_wait_game(cls, bot_logic, update_content):
        # add a new game to the db
        data = await bot_logic.api_client.create_new_game()

        # send notification to user
        game_id = data.get("game_id")
        peer_id = update_content['peer_id']
        random_id = update_content['random_id']
        from_id = update_content['from_id']

        payload = {
            'peer_id': peer_id,
            'random_id': random_id,
            'message': f'User {from_id} created a new game: {game_id}',
        }
        await cls.send(bot_logic, payload)

        # get a question from the db
        # TODO: подумать как сделать, чтобы не было повторений вопросов
        # created vshagur@gmail.com, 2021-02-11
        quiz = await bot_logic.api_client.get_quiz()

        # create keyboard
        answers = quiz.get('answers')
        correct_idx = quiz.get('correct_idx')
        question = quiz.get('question')
        timeout = quiz.get('timeout')
        round_id = 1
        keyboard = get_quiz_keyboard(from_id, game_id, answers, correct_idx, round_id)

        # ask a question
        payload = {
            'keyboard': keyboard.get_keyboard(),
            'peer_id': peer_id,
            'random_id': random_id,
            'message': f'{question}',
        }

        await cls.send(bot_logic, payload)

        # clear data for round
        bot_logic.running_games[peer_id] = {
            'round_id': round_id,
            'user_id': from_id,
            'game_id': game_id,
            'participants': [],
        }

        # set timer
        command = '/wait'
        await Command.activate_timer(bot_logic, game_id, round_id, from_id, peer_id,
                                     random_id, from_id, timeout, command)


class Grade(Command):

    @classmethod
    async def execute_if_game_in_progress(cls, bot_logic, update_content):

        # parse the result of the round
        from_id = update_content['from_id']
        peer_id = update_content['peer_id']
        date = update_content['date']

        try:
            resp_payload = json.loads(update_content.get('payload'))
            resp_game_id = resp_payload.get('game_id')
            resp_result = resp_payload.get('result')

            if resp_game_id is None or resp_result is None:
                logger.error(f'NOT_CORRECT_GAME_ID: {resp_game_id}')
                await asyncio.sleep(0)
                return

        except (TypeError, json.JSONDecodeError) as err:
            logger.error(err)
            await asyncio.sleep(0)
            return

        # check and add the result to temporary storage
        if isinstance(resp_result, bool) and resp_result:
            bot_logic.running_games[peer_id]['participants'].append((date, from_id))
        else:
            logger.error(f'BAD_VALUE_FOR_RESULT: {resp_result}')

        await asyncio.sleep(0)


class Wait(Command):

    @classmethod
    async def execute_if_game_in_progress(cls, bot_logic, update_content):
        # parse parameters
        timeout = update_content['date']
        payload = json.loads(update_content['payload'])
        command = '/move' if timeout == 0 else payload.get('command')
        game_id = payload.get('game_id')
        round_id = payload.get('round_id')
        from_id = update_content['from_id']
        peer_id = update_content['peer_id']
        random_id = update_content['random_id']

        timeout -= 1

        # set new timer
        await Command.activate_timer(bot_logic, game_id, round_id, from_id, peer_id,
                                     random_id, from_id, timeout, command)

    @classmethod
    async def execute_if_wait_game(cls, bot_logic, update_content):
        await asyncio.sleep(0)


class Move(Command):

    @classmethod
    async def execute_if_game_in_progress(cls, bot_logic, update_content):
        payload = json.loads(update_content['payload'])
        game_id = payload.get('game_id')
        peer_id = update_content['peer_id']
        random_id = update_content['random_id']
        from_id = update_content['from_id']
        round_id = payload.get('round_id')

        # get the winner of the round
        participants = bot_logic.running_games[peer_id]['participants']

        if participants:
            winner = sorted(participants, reverse=True).pop()[-1]
        else:
            winner = 0

        # save information about the winner in the db
        await bot_logic.api_client.save_round_info(game_id, round_id, winner)

        if round_id >= bot_logic.MAX_QUESTION_COUNT:

            # clear game data in temporary storage
            del bot_logic.running_games[peer_id]

            # update the game data in the db (the game is over)
            payload = {'status': 'done'}
            await bot_logic.api_client.update_game_info(game_id, payload)

            # get game result from db
            result = await bot_logic.api_client.get_result(game_id)

            # send result to user
            payload = {
                'peer_id': peer_id,
                'random_id': random_id,
                # TODO: format message
                # created vshagur@gmail.com, 2021-02-11
                'message': f'Game finished. Results: {result}',
            }

            await cls.send(bot_logic, payload)

            # send command keyboard
            await cls.send_command_keyboard(bot_logic, peer_id, random_id)

        else:
            # update round data into temporary storage
            bot_logic.running_games[peer_id]['participants'] = []
            bot_logic.running_games[peer_id]['round_id'] += 1
            round_id += 1

            # get question from database
            quiz = await bot_logic.api_client.get_quiz()

            # create quiz keyboard
            answers = quiz.get('answers')
            correct_idx = quiz.get('correct_idx')
            question = quiz.get('question')
            timeout = quiz.get('timeout')
            keyboard = get_quiz_keyboard(from_id, game_id, answers, correct_idx, round_id)

            # send quiz keyboard to user
            payload = {
                'keyboard': keyboard.get_keyboard(),
                'peer_id': peer_id,
                'random_id': random_id,
                'message': f'{question}',
            }

            await cls.send(bot_logic, payload)

            # set timer
            command = '/wait'
            await Command.activate_timer(bot_logic, game_id, round_id, from_id, peer_id,
                                         random_id, from_id, timeout, command)
