import asyncio
import json

from logger.logger import logger
from vkbot.formatters import (format_game_aborted_messages,
                              format_game_finished_messages,
                              format_top_players_message,
                              format_new_game_message)
from vkbot.keyboard import get_command_keyboard, get_quiz_keyboard


class Game:
    def __init__(self, game_id, user_id, round_id=1):
        self.game_id = game_id
        self.user_id = user_id  # game owner
        self.round_id = round_id
        self.participants = {}  # key - user_id, value - (data, result)
        self.game_players = set()

    def new_round(self):
        self.round_id += 1
        self.game_players |= set(self.participants.keys())
        self.participants = {}


class Command:
    """Base class for all commands"""

    SLEEP_TIME = 0.01

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

        await asyncio.sleep(cls.SLEEP_TIME)
        bot_logic.queue.put_nowait(timer)

    @classmethod
    async def send(cls, bot_logic, payload):
        # TODO: do refactor: add url to parameters
        # created vshagur@gmail.com, 2021-02-19
        url = bot_logic.url
        new_payload = payload.copy()
        new_payload.update(bot_logic.payload)

        async with bot_logic.session.post(url, data=new_payload) as resp:
            if resp.status == 200:
                content = await resp.json()
            else:
                logger.error(f'RESPONSE_CODE_NOT_200. URL: {url}. CODE: {resp.status}.')

    @classmethod
    async def get_user_info(cls, bot_logic, payload):
        url = 'https://api.vk.com/method/users.get'
        new_payload = payload.copy()
        new_payload.update(bot_logic.payload)

        async with bot_logic.session.post(url, data=new_payload) as resp:
            if resp.status == 200:
                return await resp.json()
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
                return

        except (TypeError, json.JSONDecodeError) as err:
            logger.error(err)
            return

        game = bot_logic.running_games.get(update_content.get('peer_id'))

        # check that the user can stop the game
        if game.user_id == update_content.get('from_id') and resp_game_id == game.game_id:
            # update the data about the game in the database (the game is over)
            payload = {'status': 0, 'game_id': game.game_id}
            await bot_logic.api_client.update_game_info(payload)

            # get game result from db
            result = await bot_logic.api_client.send_result(game.game_id,
                                                            game.game_players)

            # clear game data
            del bot_logic.running_games[update_content.get('peer_id')]

            # send game report to user
            payload = {
                'peer_id': update_content.get('peer_id'),
                'random_id': update_content.get('random_id'),
                'message': format_game_aborted_messages(result),
            }

            await cls.send(bot_logic, payload)

            # send command keyboard to user
            await cls.send_command_keyboard(
                bot_logic,
                update_content.get('peer_id'),
                update_content.get('random_id')
            )

        else:
            # send notification to user
            payload = {
                'peer_id': update_content.get('peer_id'),
                'random_id': update_content.get('random_id'),
                'message': 'Only the user who started the game can stop it.',
            }
            await cls.send(bot_logic, payload)


class Help(Command):

    @classmethod
    async def execute_if_wait_game(cls, bot_logic, update_content):
        # get help page from db
        data = await bot_logic.api_client.get_help()

        # send help page to user
        payload = {
            'peer_id': update_content.get('peer_id'),
            'random_id': update_content.get('random_id'),
            'message': data.get('text'),
        }

        await cls.send(bot_logic, payload)

        # send command keyboard
        await cls.send_command_keyboard(
            bot_logic,
            update_content.get('peer_id'),
            update_content.get('random_id')
        )


class Start(Command):

    @classmethod
    async def execute_if_game_in_progress(cls, bot_logic, update_content):
        await cls.execute_if_wait_game(bot_logic, update_content)

    @classmethod
    async def execute_if_wait_game(cls, bot_logic, update_content):
        """add new user to db"""

        user_id = update_content.get('from_id')

        # get user info
        payload = {'user_ids': str(user_id)}

        resp = await cls.get_user_info(bot_logic, payload)

        # add user to db
        user_data = resp.get('response').pop()

        data = {
            'vk_id': user_id,
            'first_name': user_data.get('first_name') or 'noname',
            'last_name': user_data.get('last_name') or 'noname',
        }

        await bot_logic.api_client.add_user(data)

        # send command keyboard to user
        await cls.send_command_keyboard(
            bot_logic,
            update_content.get('peer_id'),
            update_content.get('random_id')
        )


class Top(Command):

    @classmethod
    async def execute_if_wait_game(cls, bot_logic, update_content):
        # get report from db
        data = await bot_logic.api_client.get_top_players()

        # send report to user
        payload = {
            'peer_id': update_content.get('peer_id'),
            'random_id': update_content.get('random_id'),
            'message': format_top_players_message(data.get('users')),
        }

        await cls.send(bot_logic, payload)

        # send command keyboard to user
        await cls.send_command_keyboard(
            bot_logic,
            update_content.get('peer_id'),
            update_content.get('random_id')
        )


class NotExistCommand(Command):

    @classmethod
    async def execute_if_wait_game(cls, bot_logic, update_content):
        # send command keyboard to user
        await cls.send_command_keyboard(
            bot_logic,
            update_content.get('peer_id'),
            update_content.get('random_id')
        )


class New(Command):

    @classmethod
    async def execute_if_wait_game(cls, bot_logic, update_content):
        peer_id = update_content.get('peer_id')
        random_id = update_content.get('random_id')
        from_id = update_content.get('from_id')

        # add a new game to the db
        data = await bot_logic.api_client.create_new_game(peer_id, from_id)
        game_id = data.get('game_id')

        # create game object and add it to temp store
        game = Game(game_id, from_id)
        bot_logic.running_games[peer_id] = game

        # send notification to user
        payload = {
            'peer_id': peer_id,
            'random_id': random_id,
            'message': format_new_game_message(data),
        }

        await cls.send(bot_logic, payload)

        # get a question from the db
        # TODO: подумать как сделать, чтобы не было повторений вопросов
        # created vshagur@gmail.com, 2021-02-11
        quiz = await bot_logic.api_client.get_quiz()

        # create keyboard
        keyboard = get_quiz_keyboard(
            from_id,
            game_id,
            quiz.get('answers'),
            quiz.get('correct_idx'),
            game.round_id
        )

        # ask a question
        payload = {
            'keyboard': keyboard.get_keyboard(),
            'peer_id': peer_id,
            'random_id': random_id,
            'message': f'{quiz.get("question")}',
        }

        await cls.send(bot_logic, payload)

        # set timer
        command = '/wait'
        await Command.activate_timer(
            bot_logic, game_id, game.round_id, from_id, peer_id, random_id, from_id,
            quiz.get('timeout'), command
        )


class Grade(Command):

    @classmethod
    async def execute_if_game_in_progress(cls, bot_logic, update_content):
        # parse the result of the round
        from_id = update_content.get('from_id')
        peer_id = update_content.get('peer_id')
        random_id = update_content.get('random_id')

        try:
            resp_payload = json.loads(update_content.get('payload'))
            resp_game_id = resp_payload.get('game_id')
            resp_result = resp_payload.get('result')

            if resp_game_id is None or resp_result is None:
                logger.error(f'NOT_CORRECT_GAME_ID: {resp_game_id}')
                return

        except (TypeError, json.JSONDecodeError) as err:
            # TODO: add message
            # created vshagur@gmail.com, 2021-02-15
            logger.error(err)
            return

        # check and add the result to temporary storage
        game = bot_logic.running_games.get(peer_id)

        if not resp_game_id == game.game_id:
            logger.error('THE_WRONG_GAME_ID_WAS_SENT_IN_THE_REPLY')
            return

        if isinstance(resp_result, bool):

            if from_id in game.participants:
                # TODO: change from_id to user name
                # created vshagur@gmail.com, 2021-02-20
                payload = {
                    'peer_id': peer_id,
                    'random_id': random_id,
                    'message': f'@{from_id} The question can only be answered once.',
                }

                await cls.send(bot_logic, payload)

            else:
                game.participants[from_id] = (update_content.get('date'), resp_result)

        else:
            logger.error(f'BAD_VALUE_FOR_RESULT: {resp_result}')

        await asyncio.sleep(0)


class Wait(Command):

    @classmethod
    async def execute_if_game_in_progress(cls, bot_logic, update_content):
        timeout = update_content.get('date')
        payload = json.loads(update_content.get('payload'))
        command = '/move' if timeout <= 0 else payload.get('command')

        # set new timer
        await Command.activate_timer(
            bot_logic,
            payload.get('game_id'),
            payload.get('round_id'),
            update_content.get('from_id'),
            update_content.get('peer_id'),
            update_content.get('random_id'),
            update_content.get('from_id'),
            timeout - cls.SLEEP_TIME,
            command
        )


class Move(Command):

    @classmethod
    async def execute_if_game_in_progress(cls, bot_logic, update_content):
        payload = json.loads(update_content.get('payload'))
        game_id = payload.get('game_id')
        peer_id = update_content.get('peer_id')
        random_id = update_content.get('random_id')
        from_id = update_content.get('from_id')
        round_id = payload.get('round_id')

        # get the winner of the round
        game = bot_logic.running_games.get(peer_id)

        if game.participants:
            correct_answer_users = [(data, user_id) for user_id, (data, result) in
                                    game.participants.items() if result]

            if correct_answer_users:
                _, winner = sorted(correct_answer_users, reverse=True).pop()
            else:
                winner = 0

        else:
            winner = 0

        # save information about the winner in the db
        await bot_logic.api_client.save_round_info(game_id, round_id, winner)

        if round_id >= bot_logic.MAX_QUESTION_COUNT:

            # clear game data in temporary storage
            del bot_logic.running_games[peer_id]

            # update the game data in the db (the game is over)
            payload = {'status': 0, 'game_id': game_id}
            await bot_logic.api_client.update_game_info(payload)

            # get game result from db
            result = await bot_logic.api_client.send_result(game_id, game.game_players)

            # send result to user
            payload = {
                'peer_id': peer_id,
                'random_id': random_id,
                'message': format_game_finished_messages(result),
            }

            await cls.send(bot_logic, payload)

            # send command keyboard
            await cls.send_command_keyboard(bot_logic, peer_id, random_id)

        else:
            # update round data into temporary storage
            game.new_round()

            # get question from database
            quiz = await bot_logic.api_client.get_quiz()

            # create quiz keyboard
            keyboard = get_quiz_keyboard(
                from_id,
                game_id,
                quiz.get('answers'),
                quiz.get('correct_idx'),
                game.round_id
            )

            # send quiz keyboard to user
            payload = {
                'keyboard': keyboard.get_keyboard(),
                'peer_id': peer_id,
                'random_id': random_id,
                'message': f'{quiz.get("question")}',
            }

            await cls.send(bot_logic, payload)

            # set timer
            command = '/wait'
            await Command.activate_timer(
                bot_logic, game_id, game.round_id, from_id, peer_id, random_id,
                from_id, quiz.get('timeout'), command
            )
