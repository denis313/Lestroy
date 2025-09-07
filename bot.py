# Загружаем конфиг в переменную config
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import load_config

config = load_config()
bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

storage = MemoryStorage()
# Инициализируем бот и диспетчер
dp = Dispatcher(storage=storage)