# server/api/views.py
from aiohttp import web
from logger import logger


async def index(request):
    return web.Response(text='Hello from server!')


async def docs(request):
    if request.match_info['name'] == 'help':
        data = {'text': 'very long help page ... from db'}
        return web.json_response(data)
    else:
        raise web.HTTPNotFound()
