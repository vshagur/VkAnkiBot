import asyncio
import os

from urllib.parse import urljoin

from logger import logger


class ApiClient:

    def __init__(self, session, group_id, api_key, version, wait=25):
        self.session = session
        self.group_id = group_id
        self.version = version
        self.wait = wait
        self.api_key = api_key
        self.url = os.getenv('DB_URL')

    async def add_user(self, vk_user_id):
        url = urljoin(self.url, '/users')
        data = {'vk_user_id': vk_user_id}

        async with self.session.post(url, json=data) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                logger.error('BAD_RESPONSE_STATUS_CODE: {resp.status} from {resource}')

    async def get_help(self):
        url = urljoin(self.url, '/docs/help')

        async with self.session.get(url) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                logger.error('BAD_RESPONSE_STATUS_CODE: {resp.status} from {resource}')

    async def get_top_players(self):
        url = urljoin(self.url, '/top')

        async with self.session.get(url) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                logger.error('BAD_RESPONSE_STATUS_CODE: {resp.status} from {resource}')

    async def create_new_game(self, chat_id, vk_user_id):
        url = urljoin(self.url, '/game')
        data = {'chat_id': chat_id, 'vk_user_id': vk_user_id}

        async with self.session.post(url, json=data) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                logger.error('BAD_RESPONSE_STATUS_CODE: {resp.status} from {resource}')

    async def update_game_info(self, payload):
        url = urljoin(self.url, '/game')

        async with self.session.put(url, json=payload) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                logger.error('BAD_RESPONSE_STATUS_CODE: {resp.status} from {resource}')

    async def get_quiz(self):
        url = urljoin(self.url, '/question')

        async with self.session.get(url) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                logger.error('BAD_RESPONSE_STATUS_CODE: {resp.status} from {resource}')

    async def get_result(self, game_id):
        url = urljoin(self.url, f'/results/{game_id}')

        async with self.session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()

                game_id = data.get('game_id')
                users = data.get('users')
                score = data.get('score')

                text = f'The result of the game is {game_id}.\n'
                text += '\n'.join([f'{num}. {user}' for num, user in enumerate(users, 1)])
                text += f'\nPoints scored per game: {score}.'

                return text

            else:
                logger.error('BAD_RESPONSE_STATUS_CODE: {resp.status} from {resource}')

    async def save_round_info(self, game_id, round_id, winner):
        url = urljoin(self.url, f'/rounds/')
        data = {'vk_user_id': winner, 'game_id': game_id, 'round_id': round_id}

        async with self.session.post(url, json=data) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                logger.error('BAD_RESPONSE_STATUS_CODE: {resp.status} from {resource}')
