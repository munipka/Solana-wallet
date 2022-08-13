from aiogram import Bot, types
from aiohttp import web
from aiohttp.web_fileresponse import FileResponse
import aiohttp_jinja2
import jinja2

import config
from .utils import parse_init_data

routes = web.RouteTableDef()

def setup_template_routes(app):
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))


@routes.get("/")
async def index(request):
    balance = 42
    context = {'the_balance': balance}
    return aiohttp_jinja2.render_template("index.html", request, context)


@routes.post('/submitAmount')
async def submit_order(request):
    data = await request.json()
    init_data = parse_init_data(token=config.BOT_TOKEN, raw_init_data=data['initData'])
    if init_data is False:
        return False

    bot: Bot = request.app['bot']
    query_id = init_data['query_id']

    print(data['amount'])
    print(init_data['user'])
    return ''

    result = types.InlineQueryResultArticle(
        id=query_id,
        title='Order',
        input_message_content=types.InputTextMessageContent(message_text=result_text))
    await bot.answer_web_app_query(query_id, result)
