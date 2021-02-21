from marshmallow import Schema, fields, validate
from db.schemas import UserSchema


class RoundSchemaResponse(Schema):
    round_id = fields.Integer(required=True)


class UserSchemaRequest(Schema):
    vk_id = fields.Integer(required=True)


class DocumentSchemaResponse(Schema):
    text = fields.String(required=True)


class DocumentSchemaQuerystring(Schema):
    name = fields.String(required=True)


class TopSchemaResponse(Schema):
    users = fields.List(
        fields.Tuple(
            tuple_fields=(
                fields.Float(),
                fields.Integer(),
                fields.Integer(),
                fields.Integer(),
                fields.String(),
                fields.String(),
            )
        ))


class GameSchemaBase(Schema):
    game_id = fields.Integer()


class GameSchemaResponse(UserSchema, GameSchemaBase):
    pass
