from aiogram import Dispatcher, types

from database import user_check
from keyboard import menu, create_button, faucet_button
from wallet import get_balance


async def cmd_start(message: types.Message):
    hello_msg = 'Привет!\nСписок команд для бота:\n'
    hello_msg += 'Это тестовый бот, блабла'
    markup = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Check",
                    web_app=types.WebAppInfo(url=f'http://65.108.147.234:8001'),
                )
            ]
        ]
    )
    await message.answer("Press the button!", reply_markup=markup)
    await message.answer(text=hello_msg)


async def wallet(message: types.Message):
    """launch a wallet"""
    try:
        if user_check(message.from_user.id) is False:
            await message.answer('У вас еще нет активного кошелька. Нажмите на кнопку, чтобы создать',
                                 reply_markup=create_button())
        else:
            data = get_balance(message.from_user.id)
            public_key = data['publicKey']
            balance = data['balance']
            try:
                await message.edit_text(text=f'Ваш кошелек: {public_key}\nБаланс: {balance} SOL',
                                        reply_markup=menu())
            except:
                await message.answer(text=f'Ваш кошелек: {public_key}\nБаланс: {balance} SOL',
                                     reply_markup=menu())
    except Exception as e:
        print(e)


async def faucet(message: types.Message):
    """faucet for test tokens in a test server"""
    await message.answer(text='Чтобы получить тестовые средства, нажмите на кнопку:',
                         reply_markup=faucet_button())



def register_commands(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start")
    dp.register_message_handler(wallet, commands='wallet')
    dp.register_message_handler(faucet, commands='faucet')

