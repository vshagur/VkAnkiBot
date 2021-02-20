# server/api/views.py
from random import choice, randint
from collections import Counter

from aiohttp import web
from logger.logger import logger
from db.models import Document, User, Question, Game, Round, Statistic


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

        # add user if user is not exist
        if not user:
            await User.create(
                vk_id=vk_user_id,
                first_name=data.get('first_name'),
                last_name=data.get('last_name')
            )

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

    async def post(self):
        data = await self.request.json()
        game_id = data.get('game_id')
        game_players = data.get('game_players')

        # chose all rounds with current game_id
        game_rounds = await Round.query.where(Round.game_id == game_id).gino.all()
        # get all participants who win
        round_participants = [round_id.winner for round_id in game_rounds]

        # check case when there were no answers from the players
        if all([user_id == 0 for user_id in round_participants]):
            winners, max_score = [0, ], 0
        else:
            # delete rounds without answers
            round_participants = [user_id for user_id in round_participants if
                                  user_id != 0]
            # get winners list and max score
            counter = Counter(round_participants)
            counter.subtract()
            max_score = max(counter.values())
            winners = [user_id for user_id, score in counter.items() if
                       score == max_score]

        for user_id in game_players:

            id = await Statistic.select('id') \
                .where(Statistic.user_id == user_id) \
                .gino.scalar()

            if not id:
                user_statistic = await Statistic.create(
                    user_id=user_id,
                    total_games=0,
                    win_games=0
                )

            else:
                user_statistic = await Statistic.get(id)

            if user_id in winners:
                await user_statistic.update(
                    win_games=user_statistic.win_games + 1).apply()

            await user_statistic.update(
                total_games=user_statistic.total_games + 1).apply()

        # clear
        for game_round in game_rounds:
            await game_round.delete()

        data = {'game_id': game_id, 'users': winners, 'score': max_score}

        return web.json_response(data)


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

        round = await Round.create(
            game_id=data.get('game_id'),
            winner=data.get('vk_user_id'),
            count=data.get('round_id'),
        )

        return web.json_response({'round_id': round.id})
