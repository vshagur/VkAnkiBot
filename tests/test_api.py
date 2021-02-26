from db.models import Document, Question
from marshmallow import ValidationError
from server.api.schemas import QuestionSchemaResponse, TopSchemaResponse


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
    # check schema
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


async def test_post_question(aiohttp_client, app, restore_questions_tables,
                             questions_data):
    client = await aiohttp_client(app)
    # create new questions
    resp = await client.post('/question', json=questions_data)
    assert resp.status == 200
    data = await resp.json()
    assert 'id' in data
    assert isinstance(data.get('id'), int)


async def test_get_admin_question(aiohttp_client, app, restore_questions_tables,
                                  questions_data):
    client = await aiohttp_client(app)
    # create new questions
    resp = await client.post('/question', json=questions_data)
    resp_data = await resp.json()
    resp = await client.get(f'/admin/question/{resp_data.get("id")}')
    assert resp.status == 200
    resp_data = await resp.json()
    # check schema
    try:
        schema = QuestionSchemaResponse().load(resp_data)
    except ValidationError as err:
        assert False, f'GET request to /top return response with not valid ' \
                      f'schema \n{err.messages}'
    # check values
    assert resp_data.get('timeout') == questions_data.get('timeout')
    assert resp_data.get('correct_idx') == questions_data.get('correct_id')
    assert resp_data.get('question') == questions_data.get('question_text')
    assert resp_data.get('answers') == [questions_data.get('answer1_text'),
                                        questions_data.get('answer2_text'),
                                        questions_data.get('answer3_text'), ]


async def test_put_admin_question(aiohttp_client, app, restore_questions_tables,
                                  questions_data):
    client = await aiohttp_client(app)
    # create new question
    resp = await client.post('/question', json=questions_data)
    resp_data = await resp.json()
    idx = resp_data.get("id")
    # change data
    questions_data['correct_id'] = 3
    questions_data['answer1_text'] = 'answer1_text'
    questions_data['answer2_text'] = 'answer2_text'
    questions_data['answer3_text'] = 'answer3_text'
    questions_data['question_text'] = 'question_text'
    questions_data['timeout'] = 3
    # send put request
    resp = await client.put(f'/admin/question/{idx}', json=questions_data)
    assert resp.status == 200
    resp_data = await resp.json()
    assert resp_data == {"status": "ok"}
    # check db
    question = await Question.query.where(Question.id == idx).gino.first()
    assert question.timeout == questions_data.get('timeout')
    assert question.correct_id == questions_data.get('correct_id')
    assert question.question_text == questions_data.get('question_text')
    assert question.answer1_text == questions_data.get('answer1_text')
    assert question.answer2_text == questions_data.get('answer2_text')
    assert question.answer3_text == questions_data.get('answer3_text')
