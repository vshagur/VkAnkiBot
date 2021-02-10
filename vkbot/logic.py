import asyncio

from logger import logger
from keyboard import VkKeyboard, VkKeyboardColor, get_command_keyboard, get_quiz_keyboard


class BotLogic:
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

            # получить id беседы (peer_id) из update
            peer_id = None  # заглушка

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
            # keyboard = get_command_keyboard()
            keyboard = get_quiz_keyboard(123456, ['one', 'two', 'three', 'four'], 1)

            payload = {
                'keyboard': keyboard.get_keyboard(),
                'peer_id': update['object']['peer_id'],
                'random_id': update['object']['random_id'],
                'message': 'здесь будет вопрос',
            }

            await self.send(payload)
            # ============== конец =================

    async def send(self, payload):
        url = f'https://api.vk.com/method/messages.send'
        payload.update(self.payload)

        async with self.session.post(url, data=payload) as resp:
            if resp.status == 200:
                content = await resp.json()
            else:
                logger.error(f'RESPONSE_CODE_NOT_200. URL: {url}. CODE: {resp.status}.')
