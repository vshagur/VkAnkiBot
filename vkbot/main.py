import asyncio
import os

import aiohttp

from bot_longpoll import VkBotLongPoll
from logic import BotLogic


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
