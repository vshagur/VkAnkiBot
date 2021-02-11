import asyncio

from logger import logger


class ApiClient:

    def __init__(self, session, group_id, api_key, version, wait=25):
        self.session = session
        self.group_id = group_id
        self.version = version
        self.wait = wait
        self.api_key = api_key

    async def add_user(self, user_id):
        await asyncio.sleep(0)
        logger.debug(f'user {user_id} add to db')

    async def get_help(self):
        await asyncio.sleep(0)
        logger.debug(f'get help page from db')
        return 'help page'

    async def get_top_players(self):
        await asyncio.sleep(0)
        logger.debug(f'get top players from db')
        return 'top players'

    async def create_new_game(self):
        await asyncio.sleep(0)
        logger.debug(f'send create_new_game request to db')
        return {'game_id': 12345}

    async def get_quiz(self):
        await asyncio.sleep(0)
        logger.debug(f'get quiz from db')
        return {
            'question': 'who are you?',
            'answers': ['human', 'dog', 'cat'],
            'correct_idx': 1
        }
