import asyncio
import json

from logger import logger
from keyboard import VkKeyboard, VkKeyboardColor, get_command_keyboard, get_quiz_keyboard


class Command:
    """Base class for all commands"""

    @classmethod
    async def execute_if_game_in_progress(cls, bot_logic, update_content):
        await asyncio.sleep(0)

    @classmethod
    async def execute_if_wait_game(cls, bot_logic, update_content):
        await asyncio.sleep(0)

    @classmethod
    async def execute(cls, bot_logic, update_content):
        if cls.is_running(bot_logic, update_content):
            await cls.execute_if_game_in_progress(bot_logic, update_content)
        else:
            await cls.execute_if_wait_game(bot_logic, update_content)

    @classmethod
    def is_running(cls, bot_logic, update_content):
        return update_content.get('peer_id') in bot_logic.running_games

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
        from_id = update_content['from_id']
        peer_id = update_content['peer_id']
        random_id = update_content['random_id']

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

        user_id = bot_logic.running_games[peer_id]['user_id']
        game_id = bot_logic.running_games[peer_id]['game_id']

        if user_id == from_id and resp_game_id == game_id:
            payload = {'status': 'done'}

            await bot_logic.api_client.update_game_info(game_id, payload)
            result = await bot_logic.api_client.get_result(game_id)

            del bot_logic.running_games[peer_id]

            payload = {
                'peer_id': peer_id,
                'random_id': random_id,
                # TODO: format message
                # created vshagur@gmail.com, 2021-02-11
                'message': f'Game aborted. Results: {result}',
            }

            await cls.send(bot_logic, payload)
            await cls.send_command_keyboard(bot_logic, peer_id, random_id)

        else:
            payload = {
                'peer_id': peer_id,
                'random_id': random_id,
                'message': 'Only the user who started the game can stop it.',
            }
            await cls.send(bot_logic, payload)


class Grade(Command):

    @classmethod
    async def execute_if_game_in_progress(cls, bot_logic, update_content):
        await asyncio.sleep(0)

    @classmethod
    async def execute_if_wait_game(cls, bot_logic, update_content):
        await asyncio.sleep(0)


class Help(Command):

    @classmethod
    async def execute_if_wait_game(cls, bot_logic, update_content):
        data = await bot_logic.api_client.get_help()
        help_page = data.get('text')
        peer_id = update_content['peer_id']
        random_id = update_content['random_id']

        payload = {
            'peer_id': peer_id,
            'random_id': random_id,
            'message': help_page,
        }

        await cls.send(bot_logic, payload)
        await cls.send_command_keyboard(bot_logic, peer_id, random_id)


class Start(Command):

    @classmethod
    async def execute_if_wait_game(cls, bot_logic, update_content):
        # TODO: add getting full data about user by id
        # created vshagur@gmail.com, 2021-02-11
        from_id = update_content['from_id']
        peer_id = update_content['peer_id']
        random_id = update_content['random_id']

        await bot_logic.api_client.add_user(from_id)
        await cls.send_command_keyboard(bot_logic, peer_id, random_id)


class Top(Command):

    @classmethod
    async def execute_if_game_in_progress(cls, bot_logic, update_content):
        await asyncio.sleep(0)

    @classmethod
    async def execute_if_wait_game(cls, bot_logic, update_content):
        top_players = await bot_logic.api_client.get_top_players()

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
        await cls.send_command_keyboard(bot_logic, peer_id, random_id)


class NotExistCommand(Command):

    @classmethod
    async def execute_if_wait_game(cls, bot_logic, update_content):
        peer_id = update_content['peer_id']
        random_id = update_content['random_id']

        await cls.send_command_keyboard(bot_logic, peer_id, random_id)


class New(Command):

    @classmethod
    async def execute_if_game_in_progress(cls, bot_logic, update_content):
        await asyncio.sleep(0)

    @classmethod
    async def execute_if_wait_game(cls, bot_logic, update_content):
        data = await bot_logic.api_client.create_new_game()

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

        # TODO: подумать как сделать, чтобы не было повторений вопросов
        # created vshagur@gmail.com, 2021-02-11
        quiz = await bot_logic.api_client.get_quiz()

        answers = quiz.get('answers')
        correct_idx = quiz.get('correct_idx')
        question = quiz.get('question')

        keyboard = get_quiz_keyboard(from_id, game_id, answers, correct_idx)

        payload = {
            'keyboard': keyboard.get_keyboard(),
            'peer_id': peer_id,
            'random_id': random_id,
            'message': f'{question}',
        }

        await cls.send(bot_logic, payload)

        bot_logic.running_games[peer_id] = {
            'round': 1,
            'user_id': from_id,
            'game_id': game_id,
        }
