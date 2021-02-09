import asyncio
import os

import aiohttp

from bot_longpoll import VkBotLongPoll
from logic import BotLogic
from logger import logger


async def main():
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                group_id = os.getenv('VK_GROUP_ID')
                api_key = os.getenv('VK_API_KEY')
                version = os.getenv('VK_API_VERSION')
                debug = os.getenv('VK_BOT_MODE')
                wait = 5 if debug == '1' else 25
                queue = asyncio.Queue()
                vk_bot = VkBotLongPoll(session, queue, group_id, api_key, version, wait)
                handler = BotLogic(session, queue, group_id, api_key, version, wait)
                logger.info('BOT_START')
                logger.debug(f'BOT_PARAMETERS:')
                logger.debug(f'GROUP_ID: {group_id} ')
                logger.debug(f'API_KEY: {api_key} ')
                logger.debug(f'VERSION: {version} ')
                await asyncio.gather(vk_bot.run(), handler.run())
        except Exception as err:
            logger.error(f'BOT_RESTART_ERROR: {err}')
        finally:
            continue


if __name__ == '__main__':
    asyncio.run(main())
