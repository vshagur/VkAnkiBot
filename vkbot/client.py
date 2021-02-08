import asyncio
import logging
import os

import aiohttp

# TODO: change debug mode to info
# created vshagur@gmail.com, 2021-02-7
logging.basicConfig(
    format='[%(levelname)s] %(asctime)s: %(message)s',
    level=logging.DEBUG
)
logger = logging.getLogger("asyncio")


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
        while True:
            data = await self.queue.get()

            if data is not None:
                logger.debug(f'LONGPOLL_SERVER_RESPONSE: {data}')


class VkBotLongPoll:

    def __init__(self, session, queue, group_id, api_key, version, wait=25):
        self.session = session
        self.queue = queue
        self.group_id = group_id
        self.version = version
        self.wait = wait
        self.api_key = api_key
        self.key = None
        self.server = None
        self.ts = None

    async def update_data(self, url):
        async with self.session.get(url) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                logger.error(f'RESPONSE_CODE_NOT_200. URL: {url}. CODE: {resp.status}.')

    async def update_longpoll_server(self):

        url = f'https://api.vk.com/method/groups.getLongPollServer?' \
              f'group_id={self.group_id}&v={self.version}&access_token={self.api_key}'

        while True:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    self.key = data['response']['key']
                    self.server = data['response']['server']
                    self.ts = data['response']['ts']
                    logger.info(
                        f'LONGPOLLSERVER_DATA_UPDATED. SERVER: {self.server}. '
                        f'KEY: {self.key}. TS: {self.ts}.'
                    )
                    break
                else:
                    logger.critical(
                        f'RESPONSE_CODE_NOT_200. URL: {url}. CODE: {resp.status}.'
                    )
                    continue

    async def run(self):
        await self.update_longpoll_server()

        while True:
            url = f'{self.server}?act=a_check&key={self.key}&ts={self.ts}' \
                  f'&wait={self.wait}&access_token={self.api_key}'
            data = await self.update_data(url)
            errors = data.get('failed', None)

            # check errors
            if errors:
                logger.error(
                    f'LONGPOLL_SERVER_RETURN_ERROR. URL: {url}. RESPONSE: {data}.'
                )
                if errors == 1:
                    self.ts = data.get('ts')
                elif errors in (1, 2):
                    await self.update_longpoll_server()

            self.ts = data.get('ts')

            if data.get('updates'):
                self.queue.put_nowait(data)


async def main():
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                group_id = os.getenv('VK_GROUP_ID')
                api_key = os.getenv('VK_API_KEY')
                version = os.getenv('VK_API_VERSION')
                # TODO: delete wait, do by default
                # created vshagur@gmail.com, 2021-02-7
                wait = 5
                queue = asyncio.Queue()
                vk_bot = VkBotLongPoll(session, queue, group_id, api_key, version, wait)
                handler = BotLogic(session, queue, group_id, api_key, version, wait)
                await asyncio.gather(vk_bot.run(), handler.run())
        finally:
            continue


if __name__ == '__main__':
    asyncio.run(main())
