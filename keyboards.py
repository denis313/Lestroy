import base64
import sys
import uuid
from sys import prefix

from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


from lexicon import lexicon


# from service import bs64


# Класс для создания callback_data
class CallFactory(CallbackData, prefix='user', sep='-'):
    user_id: int
    mg: int


class CallbackFactory(CallbackData, prefix='doc', sep='-'):
    user_id: int
    mg: int


class IsIdPrepayment(CallbackData, prefix='id', sep=':'):
    payment_id: str

class Pay(CallbackData, prefix='pay', sep=':'):
    pay_id: str
    second_pay: str
    status: bool
    id_link: str

def bs_64(payment):
    uuid_obj = uuid.UUID(payment)
    # Кодирование в Base64
    compressed_uuid = base64.urlsafe_b64encode(uuid_obj.bytes).rstrip(b'=').decode('utf-8')
    return compressed_uuid


def de_bs64(compressed_uuid):
    # Декодируем из Base64
    uuid_bytes = base64.urlsafe_b64decode(compressed_uuid)
    # Преобразуем байты обратно в объект UUID
    decoded_uuid = uuid.UUID(bytes=uuid_bytes)
    return decoded_uuid


def keyboard_start():
    kb = ReplyKeyboardBuilder().row(*[KeyboardButton(text="Рассчитать стоимость"),
                                      KeyboardButton(text="О компании")], width=1)
    return kb.as_markup(resize_keyboard=True)

def keyboard_type():
    kb = ReplyKeyboardBuilder().add(*[KeyboardButton(text="Вторичка"),
                                      KeyboardButton(text="Новостройка"),
                                      KeyboardButton(text="Дом")
                                      ])
    return kb.as_markup(resize_keyboard=True)


contact_keyboard = ReplyKeyboardBuilder().add(*[KeyboardButton(text="Отправить Телефон", request_contact=True)])

# def keyboard_about():
#     kb = ReplyKeyboardBuilder().add(*[KeyboardButton(text="О компании 🏗")
#                                                     ])
#     return kb.as_markup(resize_keyboard=True)


def keyboard_project():
    kb = ReplyKeyboardBuilder().add(*[KeyboardButton(text="Да"),
                                      KeyboardButton(text="Нет")
                                      ])
    return kb.as_markup(resize_keyboard=True)
