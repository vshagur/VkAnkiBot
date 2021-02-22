# server/api/views.py
from collections import Counter
from random import randint

from aiohttp import web
from aiohttp_apispec import (docs, querystring_schema, request_schema,
                             response_schema)
from db.models import Document, Game, Question, Round, Statistic, User
from db.schemas import GameSchema, QuestionSchema, RoundSchema, UserSchema
from server.api.schemas import (DocumentSchemaQuerystring,
                                DocumentSchemaResponse, GameSchemaBase,
                                GameSchemaResponse, QuestionSchemaResponse,
                                ResultSchema, ResultSchemaResponse,
                                RoundSchemaResponse, TopSchemaResponse,
                                QuestionSchemaRequest, OkStatusSchemaResponse,
                                IdSchemaQuerystring, )


class DocumentView(web.View):

    @docs(
        tags=["doc"],
        summary="Get text document. For example: help page.",
        description="Get text document. For example: help page. .... ",
    )
    @querystring_schema(DocumentSchemaQuerystring)
    @response_schema(DocumentSchemaResponse)
    async def get(self):
        name = self.request.match_info['name']
        text = await Document.select('text').where(Document.name == name).gino.scalar()

        if text:
            return web.json_response({'text': text})

        raise web.HTTPNotFound()


class UserView(web.View):

    @docs(
        tags=["user"],
        summary="Creates a new user in the database if there is no such user yet ",
        description="Creates a new user in the database if there is no such user yet ",
    )
    @request_schema(UserSchema)
    @response_schema(UserSchema)
    async def post(self):
        data = await self.request.json()

        vk_id = data.get('vk_id')

        user = await User.select('vk_id').where(User.vk_id == vk_id).gino.scalar()

        # add user if user is not exist
        if not user:
            await User.create(
                vk_id=vk_id,
                first_name=data.get('first_name'),
                last_name=data.get('last_name')
            )

        return web.json_response({'vk_id': vk_id})


class TopView(web.View):

    @docs(
        tags=["top"],
        summary="Get top 10 of players",
        description="Get top 10 of players .... ",
    )
    @response_schema(TopSchemaResponse)
    async def get(self):
        all_users = await User \
            .join(Statistic) \
            .select().gino \
            .load(Statistic.load(user_id=User)) \
            .all()

        results = []

        for user in all_users:
            results.append((
                user.win_games / user.total_games,
                user.win_games,
                user.total_games,
                user.user_id.vk_id,
                user.user_id.first_name,
                user.user_id.last_name,
            ))

        results.sort(reverse=True)

        return web.json_response({'users': results[:10]})


class GameView(web.View):

    @docs(
        tags=["game"],
        summary="Create new game",
        description="Create new game",
    )
    @request_schema(GameSchema)
    @response_schema(GameSchemaResponse)
    async def post(self):
        data = await self.request.json()
        owner_id = data.get('owner_id')
        game = await Game.create(peer_id=data.get('peer_id'), owner_id=owner_id)
        user = await User.query.where(User.vk_id == owner_id).gino.first()

        data = {
            'game_id': game.id,
            'vk_id': owner_id,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }

        return web.json_response(data)

    @docs(
        tags=["game"],
        summary="Update game",
        description="Update game",
    )
    @request_schema(GameSchemaBase)
    @response_schema(GameSchema)
    async def put(self):
        data = await self.request.json()
        game = await Game.get(data.get('game_id'))

        if not game:
            raise web.HTTPBadRequest()

        await game.update(status=data.get('status')).apply()

        data = {
            'id': game.id,
            'status': game.status,
            'peer_id': game.peer_id,
            'owner_id': game.owner_id,
        }

        return web.json_response(data)


class ResultView(web.View):

    @docs(
        tags=["result"],
        summary="Calculate the winners of the game. Return the result.",
        description="Calculate the winners of the game. Return the result.",
    )
    @request_schema(ResultSchema)
    @response_schema(ResultSchemaResponse)
    async def post(self):
        data = await self.request.json()
        game_id = data.get('game_id')
        game_players = data.get('game_players')
        naming_dict = {}

        # chose all rounds with current game_id
        game_rounds = await Round.query.where(Round.game_id == game_id).gino.all()
        # get all participants who win
        round_participants = [round_id.winner for round_id in game_rounds]

        # check case when there were no answers from the players
        if all([user_id == 0 for user_id in round_participants]) or len(game_players) < 2:
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

            id_ = await Statistic.select('id') \
                .where(Statistic.user_id == user_id) \
                .gino.scalar()

            if not id_:
                user_statistic = await Statistic.create(
                    user_id=user_id,
                    total_games=0,
                    win_games=0
                )

            else:
                user_statistic = await Statistic.get(id_)

            if user_id in winners:
                await user_statistic.update(
                    win_games=user_statistic.win_games + 1).apply()

            await user_statistic.update(
                total_games=user_statistic.total_games + 1).apply()

            for user_id in winners:
                user = await User.query.where(User.vk_id == user_id).gino.first()
                if not user:
                    continue

                naming_dict[user_id] = {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }

        # clear
        for game_round in game_rounds:
            await game_round.delete()

        data = {
            'game_id': game_id,
            'users': winners,
            'score': max_score,
            'naming_dict': naming_dict,
        }

        return web.json_response(data)


class RoundView(web.View):

    @docs(
        tags=["round"],
        summary="Create new round",
        description="Create new round",
    )
    @request_schema(RoundSchema)
    @response_schema(RoundSchemaResponse)
    async def post(self):
        data = await self.request.json()

        game_round = await Round.create(
            game_id=data.get('game_id'),
            winner=data.get('winner'),
            count=data.get('round_id'),
        )

        return web.json_response({'round_id': game_round.id})


class QuestionView(web.View):

    @docs(
        tags=["question"],
        summary="Get data question",
        description="Get data question",
    )
    @response_schema(QuestionSchemaResponse)
    async def get(self):
        # TODO: добавить нормальное получение случайного idx
        # created vshagur@gmail.com, 2021-02-18
        MAX_QUESTION_COUNT = 3
        idx = randint(1, MAX_QUESTION_COUNT)

        question = await Question.get(idx)

        data = {
            'question': question.question_text,
            'answers': [
                question.answer1_text,
                question.answer2_text,
                question.answer3_text
            ],
            'correct_idx': question.correct_id,
            'timeout': question.timeout,
        }

        return web.json_response(data)

    @docs(
        tags=["question"],
        summary="Create new question",
        description="Create new question",
    )
    @request_schema(QuestionSchema)
    async def post(self):
        data = await self.request.json()
        question = await Question.create(**data)

        return web.json_response({'id': question.id})


class AdminQuestionView(web.View):

    @docs(
        tags=["question_admin"],
        summary="Get data question by id",
        description="Get data question by id",
    )
    @request_schema(IdSchemaQuerystring)
    @response_schema(QuestionSchemaResponse)
    async def get(self):
        question_id = self.request.match_info['id']
        question = await Question.get(int(question_id))

        if question:
            data = {
                'question': question.question_text,
                'answers': [
                    question.answer1_text,
                    question.answer2_text,
                    question.answer3_text
                ],
                'correct_idx': question.correct_id,
                'timeout': question.timeout,
            }

            return web.json_response(data)

        raise web.HTTPNotFound()

    @docs(
        tags=["question_admin"],
        summary="Update data question by id",
        description="Update data question by id",
    )
    @request_schema(QuestionSchemaRequest)
    @response_schema(OkStatusSchemaResponse)
    async def put(self):
        question_id = self.request.match_info['id']
        question = await Question.get(int(question_id))

        if not question:
            raise web.HTTPNotFound()

        data = await self.request.json()
        await question.update(**data).apply()

        return web.json_response({'status': 'ok'})

    @docs(
        tags=["question_admin"],
        summary="Delete data question by id",
        description="Delete data question by id",
    )
    @request_schema(IdSchemaQuerystring)
    @response_schema(OkStatusSchemaResponse)
    async def delete(self):
        question_id = self.request.match_info['id']
        question = await Question.get(int(question_id))

        if not question:
            raise web.HTTPNotFound()

        await question.delete()

        return web.json_response({'status': 'ok'})
