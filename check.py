from bot import bot, dp
from config import db_config
from keyboards import keyboard_start
from lexicon import lexicon

from requests import DatabaseManager
from aiogram.fsm.storage.base import StorageKey

dsn = db_config()
db_manager = DatabaseManager(dsn=dsn)

async def check_users():
    users = await db_manager.get_users()

    for user in users:
        # state = dp.storage
        # await state.set_state(StorageKey(chat_id=user.user_id, user_id=user.user_id, bot_id=bot.id), None)
        try:
            await bot.send_message(chat_id=user.user_id, text=lexicon['repeat'], reply_markup=keyboard_start())
        except:
            pass
        await db_manager.delete_user(user_id=user.user_id)