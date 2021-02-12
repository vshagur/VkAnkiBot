import asyncio
import json

from api_client import ApiClient
from logger import logger
from commands import Abort, Grade, Help, New, Start, Top, NotExistCommand


class BotLogic:
    BOT_COMMANDS = {
        '/abort': Abort,
        '/grade': Grade,
        '/help': Help,
        '/new': New,
        '/start': Start,
        '/top': Top,
        None: NotExistCommand,
    }

    MAX_QUESTION_COUNT = 10

    def __init__(self, session, queue, group_id, api_key, version, wait=25):
        self.session = session
        self.queue = queue
        self.group_id = group_id
        self.version = version
        self.wait = wait
        self.api_key = api_key
        self.payload = {
            'access_token': self.api_key,
            'group_id': self.group_id,
            'v': self.version,
        }
        self.api_client = ApiClient(session, group_id, api_key, version, wait=25)
        self.running_games = {}  # key - peer_id, value - current question number of game
        self.url = 'https://api.vk.com/method/messages.send'

    async def run(self):
        # restore game session if bot failed
        await self.get_restore_game_session()

        while True:
            update = await self.queue.get()
            logger.debug(f'GET_UPDATE_FROM_QUEUE: {update}')

            # filter by type
            resp_type = update.get('type')

            if not resp_type or resp_type != 'message_new':
                continue

            update_content = self.parse_content(update)
            command = update_content.get('command')

            await self.BOT_COMMANDS[command].execute(self, update_content)

    async def get_game_fingerprint(self):
        # TODO: add code
        # created vshagur@gmail.com, 2021-02-8
        await asyncio.sleep(0)

    async def get_restore_game_session(self):
        fingerprint = await self.get_game_fingerprint()
        # TODO: add code
        # created vshagur@gmail.com, 2021-02-8
        await asyncio.sleep(0)

    def parse_content(self, update):
        data = update.get('object')
        context = {
            'peer_id': data.get('peer_id'),
            'random_id': data.get('random_id'),
            'from_id': data.get('from_id'),
            'command': self.parse_command(data),
            'payload': data.get('payload'),
        }
        return context

    def parse_command(self, data):
        text = data.get('text')

        try:
            resp_payload = json.loads(data.get('payload'))
        except (TypeError, json.JSONDecodeError) as err:
            resp_payload = None
        except Exception as err:
            # добавил на время отладки, вдруг вылетит еще что
            resp_payload = None
            logger.error(f'NOT_AN_OBVIOUS_ERROR: {err}')

        if resp_payload and resp_payload.get('command') in self.BOT_COMMANDS:
            command = resp_payload.get('command')
        elif text in self.BOT_COMMANDS:
            command = text
        else:
            command = None

        return command
