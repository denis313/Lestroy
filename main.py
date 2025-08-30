import asyncio
import logging
from aiogram import Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import start_handler
from bot import bot
from check import check_users

# Инициализируем логгер модуля
logger = logging.getLogger(__name__)


async def main():
    # Конфигурируем логирование
    logging.basicConfig(level=logging.DEBUG,
                        filename="py_log.log",
                        filemode="w",
                        format='[%(asctime)s] #%(levelname)-8s %(filename)s:%(lineno)d - %(name)s - %(message)s')

    # Инициализируем бот и диспетчер
    dp = Dispatcher()

    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_users, 'interval', week=1)
    scheduler.start()


    # Регистриуем роутеры в диспетчере
    dp.include_router(start_handler.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("stopped")