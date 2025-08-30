from bot import bot
from config import db_config
from lexicon import lexicon
from requests import DatabaseManager


dsn = db_config()
db_manager = DatabaseManager(dsn=dsn)

async def check_users():
    users = await db_manager.get_users()
    for user in users:
        await bot.send_message(chat_id=user.user_id, text=lexicon['repeat'])
        await db_manager.delete_user(user_id=user.user_id)