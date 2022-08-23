from aiogram import Bot, types
from aiohttp import web
from aiohttp.web_fileresponse import FileResponse

from apps.wallet import get_balance, send_sol
from apps.database import select_address, save_history, update_balance_db

import config
from .utils import parse_init_data

routes = web.RouteTableDef()


@routes.get("/")
async def index(request):
    return FileResponse("static/index.html")


@routes.get("/balance")
async def load_balance(request):
    data = await get_balance(request.query["user_id"])
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

    address = await select_address(receiver)
    transaction = await send_sol(sender, amount, address[0])

    async def send_notification_to_receiver(init_data, amount):
        if 'username' in init_data['user']:
            text_receiver = 'Пользователь @' + init_data['user']['username'] + ' отправил Вам ' + str(amount) + ' Sol!'
        else:
            text_receiver = 'Пользователь ' + init_data['user']['first_name'] + ' отправил Вам ' + str(amount) + ' Sol!'
        await bot.send_message(chat_id=init_data['receiver']['id'], text=text_receiver)
    
    await send_notification_to_receiver(init_data, amount)

    # saving in history
    date = init_data['auth_date']
    try:
        name = init_data['receiver']['username']
    except:
        name = init_data['receiver']['first_name']
    await save_history(sender, name, amount, transaction, date)

    result_text = 'Вам отправили  ' + data['amount'] + ' SOL!'
    result = types.InlineQueryResultArticle(
        id=query_id,
        title='Receipt',
        input_message_content=types.InputTextMessageContent(message_text=result_text))
    await bot.answer_web_app_query(query_id, result)

    async def send_notification_to_sender(init_data, amount):
        if 'username' in init_data['receiver']:
            text = 'Вы отправили ' + str(amount) + ' Sol пользователю @' + init_data['receiver']['username']
            await bot.send_message(chat_id=init_data['user']['id'], text=text)
        else:
            text = 'Вы отправили ' + str(amount) + ' Sol пользователю ' + init_data['receiver']['first_name']
            await bot.send_message(chat_id=init_data['user']['id'], text=text)

    await send_notification_to_sender(init_data, amount)

    return web.Response(status=200)
