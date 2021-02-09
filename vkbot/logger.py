import logging

# TODO: change debug mode to info
# created vshagur@gmail.com, 2021-02-7
logging.basicConfig(
    format='[%(levelname)s] %(asctime)s: %(message)s',
    level=logging.DEBUG
)

logger = logging.getLogger("asyncio")
