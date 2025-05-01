import logging


from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, StatesGroup, State
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, FSInputFile, ReplyKeyboardRemove

from bot import bot
from keyboards import (contact_keyboard, IsIdPrepayment, keyboard_start, keyboard_type,
                       keyboard_project)
from lexicon import lexicon
from service import get_photo, IsPhone

router = Router()
router.message.filter(F.chat.type == 'private')
photo = get_photo()

@router.message(F.text.in_({'/start', 'О компании'}), StateFilter(default_state))
async def page_one(message: Message):
    await bot.send_photo(chat_id=message.from_user.id,
                         photo=photo,
                         caption=lexicon['start'], reply_markup=keyboard_start())


class Cost(StatesGroup):
    square = State()
    type_building = State()
    project = State()
    district = State()
    name = State()
    phone = State()


@router.message(F.text == 'Рассчитать стоимость')
async def calculate_cost(message: Message, state: FSMContext):
    await bot.send_message(chat_id=message.from_user.id,
                         text=lexicon['square'],
        reply_markup=None)
    await state.set_state(Cost.square)


@router.message(StateFilter(Cost.square), F.text.isdigit())
async def square(message: Message, state: FSMContext):
    await state.update_data(square=message.text)
    await bot.send_message(
        chat_id=message.chat.id, text=lexicon['type_building'],
        reply_markup=keyboard_type())
    await state.set_state(Cost.type_building)


@router.message(StateFilter(Cost.square))
async def no_square(message: Message):
    await bot.send_message(
        chat_id=message.chat.id, text=lexicon['no_square'])


@router.message(StateFilter(Cost.type_building), F.text.in_({'Вторичка', 'Новостройка', 'Дом'}))
async def type_building(message: Message, state: FSMContext):
    await state.update_data(type_building=message.text)
    await bot.send_message(
        chat_id=message.chat.id,
        text=lexicon['project'],
        reply_markup=keyboard_project())
    await state.set_state(Cost.project)


@router.message(StateFilter(Cost.type_building))
async def no_type_building(message: Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text=lexicon['no_type_building'],
        reply_markup=keyboard_type())


@router.message(StateFilter(Cost.project), F.text.in_({'Да', 'Нет'}))
async def project(message: Message, state: FSMContext):
    await state.update_data(project=message.text)
    await bot.send_message(
        chat_id=message.chat.id,
        text=lexicon['district'],
        reply_markup=ReplyKeyboardRemove())
    await state.set_state(Cost.district)


@router.message(StateFilter(Cost.project))
async def no_project(message: Message, state: FSMContext):
    await bot.send_message(
        chat_id=message.chat.id,
        text=lexicon['no_project'])


@router.message(StateFilter(Cost.district), F.text.isalpha())
async def district(message: Message, state: FSMContext):
    await state.update_data(district=message.text)
    await bot.send_message(
        chat_id=message.chat.id,
        text=lexicon['phone'],
            reply_markup=contact_keyboard.as_markup(resize_keyboard=True))
    await state.set_state(Cost.phone)


@router.message(StateFilter(Cost.district))
async def no_district(message: Message, state: FSMContext):
    await bot.send_message(
        chat_id=message.chat.id,
        text=lexicon['no_district'],
        reply_markup=None)


# @router.message(StateFilter(Cost.name), F.text.isalpha())
# async def name(message: Message, state: FSMContext):
#     await state.update_data(name=message.text)
#     await bot.send_message(
#         chat_id=message.chat.id,
#         text=lexicon['phone'],
#         reply_markup=contact_keyboard.as_markup(resize_keyboard=True))
#     await state.set_state(Cost.phone)
#
#
# @router.message(StateFilter(Cost.name))
# async def no_name(message: Message):
#     await bot.send_message(
#         chat_id=message.chat.id,
#         text=lexicon['no_name'])


@router.message(StateFilter(Cost.phone), IsPhone())
async def phone(message: Message, state: FSMContext):
    await bot.send_message(
        chat_id=message.chat.id,
        text=lexicon['end'],
        reply_markup=keyboard_start())
    try:
        if message.contact.phone_number:
            phone_number = message.contact.phone_number
    except AttributeError:
        phone_number = message.text
        if phone_number[0] == '8':
            phone_number = '+7'+ phone_number[1:]
    await state.update_data(phone=phone_number)
    data = await state.get_data()
    await state.clear()
    await bot.send_message(chat_id=message.from_user.id, text=f'Сообщение о каждом клиенте\n\n'
                               
                                f'Площадь: {data['square']}\n'
                                f'Тип жилья: {data['type_building']}\n'
                                f'Есть ли проект: {data['project']}\n'
                                f'Район: {data['district']}\n'
                                f'Телефон: {data['phone']}')


@router.message(StateFilter(Cost.phone), ~IsPhone())
async def no_phone(message: Message):
    await bot.send_message(chat_id=message.from_user.id, text=lexicon['no_phone'])
