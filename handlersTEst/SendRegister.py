from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from common import cb_menu
from database import save_history
from qrcodes import decode_qrcode
from wallet import get_balance, send_sol
from keyboard import cancel_button


class SetReceiver(StatesGroup):
    address = State()
    amount = State()
    save = State()


async def set_receiver_start(call: types.CallbackQuery):
    try:

        text = '*Внимание\!*⚠ \nПожалуйста, убедитесь, что адрес получателя *SOL* в сети *SPL*\!⚠ \n'
        text += 'Иначе, Вы можете *потерять* свои средства\n'
        text += '*Введите адрес получателя или пришлите фотографию QR\-кода:* '

        await SetReceiver.address.set()
        await call.message.edit_text(text, reply_markup=cancel_button(), parse_mode="MarkdownV2")
        await call.answer()
    except Exception as e:
        print(e)


async def address_set(message, state: FSMContext):
    try:
        await state.update_data(address_set=message.text)

        data = get_balance(message.from_user.id)
        balance = data['balance']
        text = f'Ваш текущий баланс: {balance}\nВведите сумму в SOL: '

        await SetReceiver.next()
        await SetReceiver.amount.set()
        await message.answer(text, reply_markup=cancel_button())
    except Exception as e:
        print(e)


async def address_set_photo(message, state: FSMContext):
    try:
        await message.photo[-1].download(f'users/qrcodes/from/{message.from_user.id}.png')
        address_from_qr = decode_qrcode(message.from_user.id)
        await message.delete()

        await state.update_data(address_set=address_from_qr)

        data = get_balance(message.from_user.id)
        balance = data['balance']
        text = f'Адрес отправления: {address_from_qr}\n'
        text += f'Ваш текущий баланс: {balance}\nВведите сумму в SOL: '

        await SetReceiver.next()
        await SetReceiver.amount.set()
        await message.answer(text, reply_markup=cancel_button())
    except Exception as e:
        print(e)


async def amount_set(message: types.Message, state: FSMContext):
    try:
        try:
            float(message.text)
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text='Да',
                                                    callback_data='yes_send'),
                         types.InlineKeyboardButton(text='Отмена',
                                                    callback_data=cb_menu.new(action='cancel')))
            user_data = await state.get_data()
            await message.answer(f"Отправить {message.text} SOL на адрес {user_data['address_set']}?\n",
                                 reply_markup=keyboard)
            await SetReceiver.next()
            await state.update_data(amount=float(message.text))
        except:
            await message.answer('⚠Введите число!')
            return
    except Exception as e:
        print(e)


async def set_receiver_sure(call, state: FSMContext):
    try:
        user_data = await state.get_data()
        await call.message.edit_text(text='Подождите...')
        amount = user_data['amount']
        receiver = user_data['address_set']
        transaction = send_sol(call.from_user.id, amount, receiver)
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="История транзакций",
                                                callback_data=cb_menu.new(action='history')),
                     types.InlineKeyboardButton(text='Вернуться к кошельку',
                                                callback_data=cb_menu.new(action='wallet')
                     ))
        if transaction != None:
            result = f'✅ Успешно\! \n\n ID транзакции\: `{transaction}`\n\n'
            result += 'Можете посмотреть историю отправленных транзакций, нажав на кнопку ниже\.'
            date = call.message.date
            save_history(call.from_user.id, receiver, amount, transaction, date)
            await call.message.edit_text(text=result,
                                         parse_mode="MarkdownV2",
                                         reply_markup=keyboard)
        else:
            text = '⚠ Произошла ошибка:(\nПроверьте правильность адреса и/или Ваш баланс\n'
            text += 'Также, учтите комиссию сети(~0.0005 SOL)'
            await call.message.edit_text(text=text,
                                         reply_markup=keyboard)

        await state.finish()
        await call.answer()

    except Exception as e:
        print(e)


async def cancel(call, state):
    try:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Вернуться к кошельку',
                                                callback_data=cb_menu.new(action='wallet')))
        await call.message.edit_text(text='Операция отменена!',
                                     reply_markup=keyboard)
        await state.finish()
        await call.answer()
    except Exception as e:
        print(e)


def register_state_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(set_receiver_start, cb_menu.filter(action='send_sure'))
    dp.register_message_handler(address_set, state=SetReceiver.address)
    dp.register_message_handler(address_set_photo, content_types=['photo'], state=SetReceiver.address)
    dp.register_message_handler(amount_set, state=SetReceiver.amount)
    dp.register_callback_query_handler(set_receiver_sure, text='yes_send', state=SetReceiver.save)
    dp.register_callback_query_handler(cancel, cb_menu.filter(action='cancel'), state='*')
