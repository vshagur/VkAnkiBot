import asyncio
import os
import sys

import aiohttp


class VkBotLongPoll:

    def __init__(self, group_id, api_key, version, wait=25):
        self.group_id = group_id
        self.version = version
        self.wait = wait
        self.api_key = api_key
        self.key = None
        self.server = None
        self.ts = None

    async def update_data(self, session, url):
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                # TODO: add write warning to log
                # created vshagur@gmail.com, 2021-02-6
                pass

    async def update_longpoll_server(self):

        url = f'https://api.vk.com/method/groups.getLongPollServer?' \
              f'group_id={self.group_id}&v={self.version}&access_token={self.api_key}'

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    self.key = data['response']['key']
                    self.server = data['response']['server']
                    self.ts = data['response']['ts']
                    print('call update_connection_data', data)
                else:
                    # TODO: add write warning to log
                    # created vshagur@gmail.com, 2021-02-6
                    print(resp.status)
                    sys.exit(1)

    async def run(self):
        await self.update_longpoll_server()

        async with aiohttp.ClientSession() as session:
            # TODO: change for to while
            # created vshagur@gmail.com, 2021-02-6
            for _ in range(5):
                url = f'{self.server}?act=a_check&key={self.key}&ts={self.ts}' \
                      f'&wait={self.wait}&access_token={self.api_key}'
                data = await self.update_data(session, url)
                errors = data.get('failed', None)
                # check errors
                if errors:
                    if errors == 1:
                        self.ts = data.get('ts')
                    elif errors in (1, 2):
                        await self.update_longpoll_server()

                self.ts = data.get('ts')

                print(data)


def main(group_id, api_key, version, wait=25):
    vk_bot = VkBotLongPoll(group_id, api_key, version, wait)
    asyncio.run(vk_bot.run())


if __name__ == '__main__':
    group_id = os.getenv('VK_GROUP_ID')
    api_key = os.getenv('VK_API_KEY')
    version = 5.126
    wait = 5
    main(group_id, api_key, version, wait)
