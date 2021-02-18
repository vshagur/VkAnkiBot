# server/api/views.py
from random import choice, randint

from aiohttp import web
from logger.logger import logger
from db.models import Document

QUESTIONS = (
    {
        'question': 'who are you?',
        'answers': ['human', 'bird', 'fish'],
        'correct_idx': 1,
        'timeout': 5,  # move to settings
    },
    {
        'question': 'who can read?',
        'answers': ['human', 'dog', 'cat'],
        'correct_idx': 1,
        'timeout': 5,  # move to settings
    },
    {
        'question': 'who meows?',
        'answers': ['snake ', 'dog', 'cat'],
        'correct_idx': 3,
        'timeout': 5,  # move to settings
    },
    {
        'question': 'Who catches mice??',
        'answers': ['mosquito', 'worm ', 'cat'],
        'correct_idx': 3,
        'timeout': 5,  # move to settings
    },
    {
        'question': 'Who is following the trail of criminals?',
        'answers': ['police', 'cook ', 'garcon'],
        'correct_idx': 1,
        'timeout': 5,  # move to settings
    }
)


class DocumentView(web.View):

    async def get(self):
        name = self.request.match_info['name']
        text = await Document.select('text').where(Document.name == name).gino.scalar()

        if text:
            return web.json_response({'text': text})

        raise web.HTTPNotFound()


class UserView(web.View):

    async def post(self):
        data = await self.request.json()
        vk_user_id = data.get('vk_user_id')

        if vk_user_id:
            logger.debug(f'add user: {vk_user_id} to db')
            # TODO: add logic
            # created vshagur@gmail.com, 2021-02-14
            # проверить сначала, что такого пользователя еще нет
            data = {'user_id': 1111111}  # dummy

            return web.json_response(data)

        raise web.HTTPBadRequest()


class TopView(web.View):

    async def get(self):
        # TODO: add logic
        # created vshagur@gmail.com, 2021-02-14
        data = {'users': {'Ivan': 20, 'Oleg': 19}}
        logger.debug(f'get top players from db: {data}')

        return web.json_response(data)


class GameView(web.View):

    async def post(self):
        data = await self.request.json()
        chat_id = data.get('chat_id')
        vk_user_id = data.get('vk_user_id')

        if vk_user_id and chat_id:
            # TODO: add logic
            # created vshagur@gmail.com, 2021-02-14
            game_id = randint(10 ** 4, 10 ** 5 - 1)
            data = {'game_id': game_id}  # dummy

            logger.debug(f'new game created: {game_id} to db')
            return web.json_response(data)

        raise web.HTTPBadRequest()

    async def put(self):
        data = await self.request.json()
        game_id = data.get('game_id')
        status = data.get('status')

        if game_id:
            # TODO: add logic
            # created vshagur@gmail.com, 2021-02-14
            data = {
                'game_id': game_id,
                # 'vk_user_id': 'vk_user_id from db',
                # 'chat_id': 'chat_id from db',
                'status': status,
            }  # dummy

            logger.debug(f'game info updated: {data}')
            return web.json_response(data)

        raise web.HTTPBadRequest()


class ResultView(web.View):

    async def get(self):
        game_id = self.request.match_info['game_id']

        if game_id:
            # TODO: add logic
            # created vshagur@gmail.com, 2021-02-14
            data = {'game_id': game_id, 'users': ['Ivan', 'Oleg'], 'score': randint(2, 4)}
            logger.debug(f'get game result from db: {data}')

            return web.json_response(data)

        raise web.HTTPNotFound()


class QuestionView(web.View):

    async def get(self):
        # TODO: add logic
        # created vshagur@gmail.com, 2021-02-14
        data = choice(QUESTIONS)
        logger.debug(f'get question from db: {data}')

        return web.json_response(data)


class RoundView(web.View):

    async def post(self):
        data = await self.request.json()
        vk_user_id = data.get('vk_user_id')
        game_id = data.get('game_id')
        round_id = data.get('round_id')

        if vk_user_id and game_id and round_id:
            # TODO: add logic
            # created vshagur@gmail.com, 2021-02-14
            data = {'round_id': randint(10 ** 3, 10 ** 4 - 1)}  # dummy
            logger.debug(f'add round: {round_id} to db')

            return web.json_response(data)

        raise web.HTTPBadRequest()
