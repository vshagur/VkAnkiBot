# server/api/views.py
from random import choice, randint

from aiohttp import web
from logger.logger import logger
from db.models import Document, User, Question, Game, Round

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
        user = await User.select('vk_id').where(User.vk_id == vk_user_id).gino.scalar()

        if not user:
            await User.create(vk_id=vk_user_id)

        return web.json_response({'user_id': vk_user_id})


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

        game = await Game.create(
            peer_id=data.get('chat_id'),
            owner_id=data.get('vk_user_id')
        )

        return web.json_response({'game_id': game.id})

    async def put(self):
        data = await self.request.json()
        game = await Game.get(data.get('game_id'))

        if not game:
            raise web.HTTPBadRequest()

        await game.update(status=data.get('status')).apply()

        data = {
            'game_id': game.id,
            'status': game.status,
            'peer_id': game.peer_id,
            'owner_id': game.owner_id,
        }

        return web.json_response(data)


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
        # TODO: добавить нормальное получение случайного idx
        # created vshagur@gmail.com, 2021-02-18
        db_max = 3
        idx = randint(1, 3)

        question = await Question.get(idx)

        data = {
            'question': question.question_text,
            'answers': [
                question.answer1_text,
                question.answer2_text,
                question.answer3_text
            ],
            'correct_idx': question.correct_id,
            # TODO: добавить в базу значений с timeout
            # created vshagur@gmail.com, 2021-02-18
            'timeout': 5,  # move to settings
        }

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
