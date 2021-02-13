import logging
import os

DEBUG = os.getenv('VK_BOT_MODE')

logging.basicConfig(
    format='[%(levelname)s] %(asctime)s: %(message)s',
    level=logging.DEBUG if DEBUG == '1' else logging.INFO
)

logger = logging.getLogger("asyncio")
