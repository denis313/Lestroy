from aiogram.types import Message, CallbackQuery
import re
from aiogram.types import FSInputFile
from aiogram.filters import BaseFilter


def get_photo():
    photo = FSInputFile(f'photo_2025-04-09_21-46-40.png', filename=f'photo_img')
    return photo


class IsPhone(BaseFilter):
    async def __call__(self, message: Message):
        try:
            if message.contact.phone_number:
                return True
        except AttributeError:
            match = re.fullmatch(r'\\8\d{3}\d{7}', message.text)
            return bool(match)