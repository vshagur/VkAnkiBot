from db.models import Document
from marshmallow import ValidationError
from server.api.schemas import (QuestionSchemaResponse, TopSchemaResponse, )


async def test_get_help(api_test_client):
    resp = await api_test_client.get('/docs/help')
    assert resp.status == 200
    data = await resp.json()
    expected = await Document.query.where(Document.name == 'help').gino.first()
    assert data.get('text') == expected.text


async def test_get_question_random_return_valid_schema(api_test_client):
    resp = await api_test_client.get('/question')
    assert resp.status == 200
    data = await resp.json()

    try:
        schema = QuestionSchemaResponse().load(data)
    except ValidationError as err:
        assert False, f'GET request to /question return response with not valid ' \
                      f'schema \n{err.messages}'


async def test_get_top_return_valid_schema(api_test_client):
    resp = await api_test_client.get('/top')
    assert resp.status == 200
    data = await resp.json()

    try:
        schema = TopSchemaResponse().load(data)
    except ValidationError as err:
        assert False, f'GET request to /top return response with not valid ' \
                      f'schema \n{err.messages}'


async def test_post_question(aiohttp_client, app):
    client = await aiohttp_client(app)
    data = {
        "timeout": 3,
        "correct_id": 1,
        "answer1_text": "human123456789",
        "answer3_text": "dog",
        "question_text": "who are you?",
        "answer2_text": "cat"
    }
    resp = await client.post('/question', json=data)
    assert resp.status == 200
    data = await resp.json()
    assert 'id' in data
    assert isinstance(data.get('id'), int)
