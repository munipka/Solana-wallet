from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from SImpleTest.common import cb_menu


def create_button():
    """make a 'create' button for a new wallet"""
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text='Создать', callback_data=cb_menu.new(action='create'))
    keyboard.add(button)
    return keyboard


def go_to_wallet():
    """make 'go to your wallet' button"""
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text='Перейти к кошельку', callback_data=cb_menu.new(action='wallet'))
    keyboard.add(button)
    return keyboard


def menu():
    """makes inline-buttons for the MAIN menu"""
    keyboard = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton(text="Получить", callback_data=cb_menu.new(action="receive")),
        InlineKeyboardButton(text="Отправить", callback_data=cb_menu.new(action="send"))
    ]
    keyboard.add(*buttons)
    keyboard.add(InlineKeyboardButton(text='Обменять(dev.)', callback_data='exchange'),
                 InlineKeyboardButton(text='Обновить', callback_data=cb_menu.new(action='reload')))
    keyboard.add(InlineKeyboardButton(text='История транзакций', callback_data=cb_menu.new(action='history')))
    return keyboard


def receive_menu():
    """makes inline-buttons for RECEIVE menu"""
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Создать QR-код", callback_data=cb_menu.new(action='qrcode')),
                 InlineKeyboardButton(text='<- Назад', callback_data=cb_menu.new(action='wallet')))
    return keyboard


def send_menu():
    """makes inline-buttons for SEND menu"""
    keyboard = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton(text='Продолжить', callback_data=cb_menu.new(action='send_sure')),
        InlineKeyboardButton(text='<-Назад', callback_data=cb_menu.new(action='wallet')),
    ]
    keyboard.add(*buttons)
    return keyboard


def cancel_button():
    """makes cancel button"""
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='Отмена', callback_data=cb_menu.new(action='cancel')))
    return keyboard


def faucet_button():
    """creates faucet button"""
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='Прислать 2 Sol', callback_data=cb_menu.new(action='faucet')))
    return keyboard
