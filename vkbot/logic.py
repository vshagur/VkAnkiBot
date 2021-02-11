import asyncio
import json

from logger import logger
from keyboard import VkKeyboard, VkKeyboardColor, get_command_keyboard, get_quiz_keyboard


class BotLogic:
    BOT_COMMANDS = ('/abort', 'grade', '/help', '/new', '/start', '/top')

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

        self.running_game_chats = []

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

            # =========== filter by type ============
            resp_type = update.get('type')

            if not resp_type or resp_type != 'message_new':
                continue

            # =========== parse =====================
            data = update.get('object')
            peer_id = data.get('peer_id')
            random_id = data.get('random_id')
            text = data.get('text')
            command = self.parse_command(data)

            if peer_id in self.running_game_chats:
                # игра запущена, обработать случаи:
                # 1. пользователь остановил игру (/abort)
                #    - запрос в базу данных об игре (для получения пользователя,
                #      запустившего игру)
                #    - проверка, что пользователь совпадает, если нет - ??? (подумать)
                #    - запрос в базу данных на изменения статуса игры (finished)
                #    - запрос в базу данных на получение результата игры
                #    - удалить id чата из running_game_chats
                #    - отправить результат в сообщении
                #    - отправить клавиатуру команд
                # 2. пользователь дал неправильный ответ
                #    - переходим к следующему сообщению
                # 3. пользователь дал правильный ответ
                #    - делаем запрос на обновление игры (добавляем id победителя
                #    в текущем раунде)
                #    - если вопрос был последним, то выполняем действия из пункта 1,
                #      в противном случае выполняем послединие 4 действия из пункта 5
                #      в ветке для случая, когда игра не запущена
                # 4. другие случаи (подумать на какие команды нужно послать сообещния,
                #    а какие проигнорировать)
                pass
            else:
                # игра не запущена, обработать случаи:
                # 1. пользователь добавился в группу (/start)
                #    - добавить пользователя в базу
                #    - отправить клавиатуру команд
                # 2. пользователь вызвал справку по игре (/help)
                #    - получить из базы справку
                #    - отправить справку в сообщении
                #    - отправить клавиатуру команд
                # 3. пользователь запросил топ игроков (/top)
                #    - запросить из базы топ игроков
                #    - отправитьтоп игроков в сообщении
                #    - отправить клавиатуру команд
                # 4. пользователь запустил новую игру (/new)
                #    - выполнить запрос к базе на создание новой игры (вернется id +
                #      количество вопросов, подумать)
                #    - отправить сообщение о старте новой игры
                #    - выполнить запрос к базе на получение нового вопроса
                #    - создать клавиатуру вопроса
                #    - добавить id беседы в running_game_chats
                #    - отправить клавиатуру вопроса
                # 5. другие сообщения (например, ответы с предыдущих вопросов или
                # просто сообщения пользователей не относящиеся к игре)
                pass

            # ============== отладка ================
            logger.debug(f'user send command: {command}')
            await self.send_command_keyboard(peer_id, random_id)
            # ============== конец =================

    async def send(self, payload):
        url = f'https://api.vk.com/method/messages.send'
        payload.update(self.payload)

        async with self.session.post(url, data=payload) as resp:
            if resp.status == 200:
                content = await resp.json()
            else:
                logger.error(f'RESPONSE_CODE_NOT_200. URL: {url}. CODE: {resp.status}.')

    async def send_command_keyboard(self, peer_id, random_id):
        keyboard = get_command_keyboard()
        payload = {
            'keyboard': keyboard.get_keyboard(),
            'peer_id': peer_id,
            'random_id': random_id,
            'message': ('Choose an action:\n'
                        '"Help" - get help about the game\n'
                        '"Top Players" - Bring out the top 10 players\n'
                        '"Start game" - create a new game')
        }

        await self.send(payload)

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
