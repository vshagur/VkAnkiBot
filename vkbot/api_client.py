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
        return {'text': 'Very long game description ...'}

    async def get_top_players(self):
        await asyncio.sleep(0)
        logger.debug(f'get top players from db')
        return 'top players'

    async def create_new_game(self):
        await asyncio.sleep(0)
        logger.debug(f'create new game into db')
        return {'game_id': 12345}

    async def get_game_info(self, game_id):
        await asyncio.sleep(0)
        logger.debug(f'get game info from db')
        return {'game_id': 12345, 'user_id': 436740675}

    async def update_game_info(self, game_id, payload):
        await asyncio.sleep(0)
        logger.debug(f'update game info into db')
        return {'game_id': 12345}

    async def get_quiz(self):
        await asyncio.sleep(0)
        logger.debug(f'get quiz from db')
        return {
            'question': 'who are you?',
            'answers': ['human', 'dog', 'cat'],
            'correct_idx': 1
        }

    async def get_result(self, game_id):
        await asyncio.sleep(0)
        logger.debug(f'get result game by game_id from db')
        return {'game_id': game_id, 'winтers': ['Ivan', 'Oleg'], 'score': 5}
