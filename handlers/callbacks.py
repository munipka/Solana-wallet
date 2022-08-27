from aiogram import types, Dispatcher
from aiogram.types import InputFile

from apps.common import cb_menu
from apps.database import user_check, add_user, get_history
from apps.qrcodes import make_qrcode
from apps.wallet import get_balance, fund_account, create_wallet
from apps.keyboard import go_to_wallet, create_button, menu, receive_menu, send_menu


async def message_create_wallet(call: types.CallbackQuery):
    """Callback handler that creates a wallet for a new user"""
    try:
        new_wallet = await create_wallet(call.from_user.id)
        await call.message.edit_text(text=f'Кошелек создан, Ваш адрес: `{new_wallet}` ',
                                     parse_mode='MarkdownV2',
                                     reply_markup=go_to_wallet())
        await add_user(call.from_user.id)
        await call.answer()
    except Exception as e:
        print(e)


async def wallet(call: types.CallbackQuery):
    """Handler that launches a wallet, but from a call"""
    try:
        if await user_check(call.from_user.id) is False:
            await call.message.answer('У вас еще нет активного кошелька. Нажмите на кнопку, чтобы создать',
                                      reply_markup=create_button())
        else:
            data = await get_balance(call.from_user.id)
            public_key = data['publicKey']
            balance = data['balance']
            try:
                await call.message.edit_text(text=f'Ваш кошелек: {public_key}\nБаланс: {balance} SOL',
                                             reply_markup=menu())
            except:
                await call.message.answer(text=f'Ваш кошелек: {public_key}\nБаланс: {balance} SOL',
                                          reply_markup=menu())
        await call.answer()
    except Exception as e:
        print(e)


async def receive(call: types.CallbackQuery):
    """RECEIVE menu callback handler"""
    try:
        data = await get_balance(call.from_user.id)
        address = data['publicKey']
        text = "Чтобы отправитель мог отправить вам средства, ему необходимо знать адрес вашего кошелька\.\n\n"
        text += "*Внимание\!* Отправляйте на этот адрес *только SOL сеть SPL*, иначе Вы *потеряете* Ваши средства\!⚠\n\n"
        text += f"Чтобы скопировать адрес, *просто нажмите* на него: \n\n `{address}`\n\n"
        text += "Также, можно получить QR\-код вашего адреса, нажав на кнопку ниже\."
        try:
            await call.message.edit_text(text=text,
                                         parse_mode='MarkdownV2',
                                         reply_markup=receive_menu())
        except:
            await call.message.delete()
            await call.message.answer(text=text,
                                      parse_mode='MarkdownV2',
                                      reply_markup=receive_menu())
        await call.answer()
    except Exception as e:
        print(e)


async def create_qrcode(call: types.CallbackQuery):
    """Callback handler that creates qrcode of user`s address"""
    await call.message.delete()
    data = await get_balance(call.from_user.id)
    address = data['publicKey']
    qrcode_path = make_qrcode(call, address)
    photo = InputFile(qrcode_path)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='<- Назад', callback_data=cb_menu.new(action='receive')))
    await call.message.answer_photo(photo=photo, reply_markup=keyboard)
    await call.answer()


async def send(call: types.CallbackQuery):
    """SEND menu callback handler"""
    try:
        text = 'Чтобы отправить средства, Вам нужно будет ввести или прислать QR\-код адреса получателя *SOL* в сети *SPL*,'
        text += ' а также сумму перевода\. \n'
        text += 'По завершении транзакции, Вы получите ее id\.'
        await call.message.edit_text(text=text,
                                     parse_mode="MarkdownV2",
                                     reply_markup=send_menu())
    except Exception as e:
        print(e)
    await call.answer()


async def wallet_reload(call: types.CallbackQuery):
    """reload the wallet callback handler"""
    await call.message.delete()
    await wallet(call)
    await call.answer()


async def faucet(call: types.CallbackQuery):
    """FAUCET for test server callback handler"""
    await fund_account(call.from_user.id, amount=2)
    await call.message.edit_text(text="Тестовые токены отправлены!\n/wallet - кошелек")
    await call.answer()


async def show_history(call: types.CallbackQuery):
    """Callback handler that shows last 5 sent transactions"""
    try:
        data = await get_history(call.from_user.id)
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Вернуться к кошельку',
                                                callback_data=cb_menu.new(action='wallet')))
        text = '*Последние 5 отправленных Вами транзакций*\n'
        for item in data:
            if len(item[0]) > 15:
                text += '\n*Получатель:* ' + '`' + item[0] + '`'
            else:
                text += '\n*Получатель:* ' + '`' + 'Telegram user: @' + item[0] + '`'
            text += '\n*Количество:* ' + str(item[1]) + ' SOL'
            text += '\n*ID транзакции:* ' + '`' + item[2] + '`'
            text += '\n\n '
        await call.message.edit_text(text=text.replace(".", "\\."),
                                     parse_mode="MarkdownV2",
                                     reply_markup=keyboard)
        await call.answer()
    except Exception as e:
        print(e)


def register_callbacks(dp: Dispatcher):
    """register callbacks"""
    dp.register_callback_query_handler(message_create_wallet, cb_menu.filter(action='create'))
    dp.register_callback_query_handler(wallet, cb_menu.filter(action='wallet'))
    dp.register_callback_query_handler(receive, cb_menu.filter(action='receive'))
    dp.register_callback_query_handler(create_qrcode, cb_menu.filter(action='qrcode'))
    dp.register_callback_query_handler(send, cb_menu.filter(action='send'))
    dp.register_callback_query_handler(wallet_reload, cb_menu.filter(action='reload'))
    dp.register_callback_query_handler(show_history, cb_menu.filter(action='history'))
    dp.register_callback_query_handler(faucet, cb_menu.filter(action='faucet'))
