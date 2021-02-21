import os
from urllib.parse import urljoin

from logger.logger import logger


class ApiClient:

    def __init__(self, session, group_id, api_key, version, wait=25):
        self.session = session
        self.group_id = group_id
        self.version = version
        self.wait = wait
        self.api_key = api_key
        self.url = os.getenv('DB_URL')

    async def add_user(self, data):
        url = urljoin(self.url, '/users')

        return await self.make_request(self.session.post(url, json=data))

    async def get_help(self):
        url = urljoin(self.url, '/docs/help')

        return await self.make_request(self.session.get(url))

    async def get_top_players(self):
        url = urljoin(self.url, '/top')

        return await self.make_request(self.session.get(url))

    async def create_new_game(self, chat_id, vk_user_id):
        url = urljoin(self.url, '/game')
        data = {'chat_id': chat_id, 'vk_user_id': vk_user_id}

        return await self.make_request(self.session.post(url, json=data))

    async def update_game_info(self, payload):
        url = urljoin(self.url, '/game')

        return await self.make_request(self.session.put(url, json=payload))

    async def get_quiz(self):
        url = urljoin(self.url, '/question')

        return await self.make_request(self.session.get(url))

    async def send_result(self, game_id, game_players):
        url = urljoin(self.url, '/results')
        data = {'game_id': game_id, 'game_players': list(game_players)}

        return await self.make_request(self.session.post(url, json=data))

    async def save_round_info(self, game_id, round_id, winner):
        url = urljoin(self.url, f'/rounds')
        data = {'winner': winner, 'game_id': game_id, 'round_id': round_id}

        return await self.make_request(self.session.post(url, json=data))

    async def make_request(self, coroutine):

        async with coroutine as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                logger.error(f'BAD_RESPONSE_STATUS_CODE: {resp.status} ')
