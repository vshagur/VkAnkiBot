from logger import logger


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

    async def get_update(self, url):
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
            # get updates
            url = f'{self.server}?act=a_check&key={self.key}&ts={self.ts}' \
                  f'&wait={self.wait}&access_token={self.api_key}'
            data = await self.get_update(url)

            # check errors
            errors = data.get('failed', None)

            if errors:
                logger.error(
                    f'LONGPOLL_SERVER_RETURN_ERROR. URL: {url}. RESPONSE: {data}.'
                )
                if errors == 1:
                    self.ts = data.get('ts')
                elif errors in (1, 2):
                    await self.update_longpoll_server()

                continue

            # set new ts value and send updates to queue
            self.ts = data.get('ts')
            updates = data.get('updates')

            # add updates to queue
            if updates:
                for update in updates:
                    self.queue.put_nowait(update)
