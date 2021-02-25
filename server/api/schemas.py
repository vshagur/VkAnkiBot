from db.schemas import UserSchema
from marshmallow import Schema, fields, validate

# TODO: move MAXQUESTION to settings
# created vshagur@gmail.com, 2021-02-21
MAXQUESTION = 3


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


class ResultSchema(GameSchemaBase):
    game_players = fields.List(fields.Integer())


class ResultSchemaResponse(GameSchemaBase):
    users = fields.List(fields.Integer())
    score = fields.Integer()
    naming_dict = fields.Dict(
        keys=fields.Integer(),
        values=fields.Dict(
            keys=fields.String(
                validate=validate.OneOf(['first_name', 'last_name']),
                values=fields.String()
            )))


class QuestionSchemaResponse(GameSchemaBase):
    question = fields.String()
    answers = fields.List(fields.String, validate=validate.Length(equal=MAXQUESTION))
    correct_idx = fields.Integer()
    timeout = fields.Integer()


class QuestionSchemaRequest(Schema):
    question_text = fields.String()
    answer1_text = fields.String()
    answer2_text = fields.String()
    answer3_text = fields.String()
    correct_id = fields.Integer()
    timeout = fields.Integer()


class OkStatusSchemaResponse(Schema):
    status = fields.String(
        required=True,
        validate=validate.OneOf(['ok', ])
    )


class IdSchemaQuerystring(Schema):
    id = fields.Integer(required=True)
