from aiogram import Bot, types
from aiohttp import web
from aiohttp.web_fileresponse import FileResponse
import aiohttp_jinja2
import jinja2

from wallet import get_balance, send_sol
from database import select_address, save_history

import config
from .utils import parse_init_data

routes = web.RouteTableDef()

def setup_template_routes(app):
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))


@routes.get("/")
async def index(request):
    return FileResponse("static/index.html")


@routes.get("/balance")
async def load_balance(request):
    data=get_balance(request.query["user_id"])
    balance = data['balance']
    return web.Response(text=balance)
    

@routes.post('/submitAmount')
async def submit_order(request):
    data = await request.json()
    init_data = parse_init_data(token=config.BOT_TOKEN, raw_init_data=data['initData'])
    if init_data is False:
        return False

    bot: Bot = request.app['bot']
    query_id = init_data['query_id']
    sender = init_data['user']['id']
    receiver = init_data['receiver']['id']
    amount = float(data['amount'])

    print(init_data)
    address = select_address(receiver)
    transaction = send_sol(sender, amount, address[0])

    
    #saving in history
    date = init_data['auth_date']
    try:
        name = init_data['receiver']['username']
    except:
        name = init_data['receiver']['first_name']
    save_history(sender, name, amount, transaction, date)
    
    result_text = 'Вам отправили  ' + data['amount'] + ' SOL!'
    result = types.InlineQueryResultArticle(
        id=query_id,
        title='Receipt',
        input_message_content=types.InputTextMessageContent(message_text=result_text))
    await bot.answer_web_app_query(query_id, result)
    
    
    if 'username' in init_data['receiver']:
        print('1')
        text = 'Вы отправили ' + str(amount) + ' Sol пользователю @' + init_data['receiver']['username']
    else:
        print('2')
        text = 'Вы отправили ' + str(amount) + ' Sol пользователю ' + init_data['receiver']['first_name']    
    
    if 'username' in init_data['user']:
        print('3')
        text_receiver = 'Пользователь @' + init_data['user']['username'] + ' отправил Вам ' + str(amount) + ' Sol!'
    else:
        print('4')
        text_receiver = 'Пользователь ' + init_data['user']['first_name'] + ' отправил Вам ' + str(amount) + ' Sol!'
    print(receiver)
    
    await bot.send_message(chat_id = receiver, text=text_receiver)
    await bot.send_message(chat_id = sender, text=text)
    
    return web.Response(status=200)
    
    

