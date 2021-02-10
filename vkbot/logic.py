import asyncio
import uuid

from keyboard import VkKeyboard

from logger import logger


class BotLogic:
    def __init__(self, session, queue, group_id, api_key, version, wait=25):
        self.session = session
        self.queue = queue
        self.group_id = group_id
        self.version = version
        self.wait = wait
        self.api_key = api_key

    async def get_game_fingerprint(self):
        # TODO: add code
        # created vshagur@gmail.com, 2021-02-8
        await asyncio.sleep(0)

    async def get_restore_game_session(self):
        fingerprint = await self.get_game_fingerprint()
        # TODO: add code
        # created vshagur@gmail.com, 2021-02-8
        await asyncio.sleep(0)

    async def run(self):
        # restore game session if bot failed
        await self.get_restore_game_session()

        while True:
            data = await self.queue.get()

            if data is not None:
                logger.debug(f'LONGPOLL_SERVER_RESPONSE: {data}')
                keyboard = VkKeyboard()
                keyboard.add_text_button('primary', 'some text for button1',
                                         "{\"button\": \"1\"}")
                keyboard.add_text_button('negative', 'some text for button2',
                                         "{\"button\": \"2\"}")
                # keyboard = '{"buttons":[],"one_time":true}'
                url = f'https://api.vk.com/method/messages.send'
                payload = {
                    'keyboard': keyboard.get_keyboard(),
                    # 'keyboard': keyboard,
                    'access_token': self.api_key,
                    'group_id': self.group_id,
                    'peer_id': data['updates'][0]['object']['peer_id'],
                    'v': self.version,
                    # 'random_id': uuid.uuid1().int >> 64,
                    'random_id': data['updates'][0]['object']['random_id'],
                    'message': 'hi, from bot',
                }
                async with self.session.post(url, data=payload) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        logger.debug(f'RESPONSE: {data}')
