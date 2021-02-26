from db.models import Document
from marshmallow import ValidationError
from server.api.schemas import QuestionSchemaResponse


async def test_get_help(test_client, app):
    client = await test_client(app)
    resp = await client.get('/docs/help')

    assert resp.status == 200

    data = await resp.json()
    expected = await Document.query.where(Document.name == 'help').gino.first()

    assert data.get('text') == expected.text


async def test_get_question_random_return_valid_schema(test_client, app):
    client = await test_client(app)
    resp = await client.get('/question')

    assert resp.status == 200

    data = await resp.json()

    try:
        schema = QuestionSchemaResponse().load(data)
    except ValidationError as err:
        assert False, f'GET request to /question return response with not valid ' \
                      f'schema \n{err.messages}'
