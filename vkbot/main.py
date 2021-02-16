import asyncio
import os

import aiohttp
from logger.logger import logger
from vkbot.bot_longpoll import VkBotLongPoll
from vkbot.logic import BotLogic


def get_configuration():
    group_id = os.getenv('VK_GROUP_ID')
    api_key = os.getenv('VK_API_KEY')
    version = os.getenv('VK_API_VERSION')
    debug = os.getenv('VK_BOT_MODE')
    wait = 5 if debug == '1' else 25

    return group_id, api_key, version, debug, wait


async def main():
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                group_id, api_key, version, debug, wait = get_configuration()
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
            await session.close()
        finally:
            continue


if __name__ == '__main__':
    asyncio.run(main())
