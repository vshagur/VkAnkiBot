from marshmallow import Schema, fields, validate


class GameSchema(Schema):
    id = fields.Integer()
    peer_id = fields.Integer(required=True)
    owner_id = fields.Integer(required=True)
    status = fields.Integer(validate=validate.OneOf([0, 1]))


class UserSchema(Schema):
    vk_id = fields.Integer(required=True)
    first_name = fields.String()
    last_name = fields.String()


class RoundSchema(Schema):
    id = fields.Integer()
    game_id = fields.Integer(required=True)
    count = fields.Integer(required=True)
    winner = fields.Integer(required=True)


class DocumentSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    text = fields.String()


class StatisticSchema(Schema):
    id = fields.Integer()
    user_id = fields.Integer()
    total_games = fields.Integer()
    win_games = fields.Integer()
