import asyncio

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
            update = await self.queue.get()
            # TODO: add logic
            # created vshagur@gmail.com, 2021-02-10
            logger.debug(f'GET_UPDATE_FROM_QUEUE: {update}')
