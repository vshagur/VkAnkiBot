from marshmallow import Schema, fields


class RoundSchemaResponse(Schema):
    round_id = fields.Integer(required=True)


class UserSchemaRequest(Schema):
    vk_id = fields.Integer(required=True)


class DocumentSchemaResponse(Schema):
    text = fields.String(required=True)


class DocumentSchemaQuerystring(Schema):
    name = fields.String(required=True)
