import asyncio

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
        await asyncio.sleep(0)

    @classmethod
    async def execute_if_wait_game(cls, bot_logic, update_content):
        await asyncio.sleep(0)


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


class New(Command):

    @classmethod
    async def execute_if_game_in_progress(cls, bot_logic, update_content):
        await asyncio.sleep(0)

    @classmethod
    async def execute_if_wait_game(cls, bot_logic, update_content):
        await asyncio.sleep(0)


class Start(Command):

    @classmethod
    async def execute_if_wait_game(cls, bot_logic, update_content):
        peer_id = update_content['peer_id']
        random_id = update_content['random_id']

        await cls.send_command_keyboard(bot_logic, peer_id, random_id)


class Top(Command):

    @classmethod
    async def execute_if_game_in_progress(cls, bot_logic, update_content):
        await asyncio.sleep(0)

    @classmethod
    async def execute_if_wait_game(cls, bot_logic, update_content):
        await asyncio.sleep(0)
