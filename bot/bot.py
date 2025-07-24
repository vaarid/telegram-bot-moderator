import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode, UpdateType
from aiogram.client.default import DefaultBotProperties

from utils import load_env
from logging_config.config import setup_logging
from handlers import setup_handlers
from filters import ProfanityFilter
from utils.db import create_table, init_pool

# Загрузка переменных окружения
load_env()

# Настройка логирования
setup_logging()
logger = logging.getLogger(__name__)

# Получение токена
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Инициализация бота и диспетчера
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Регистрация фильтров и хендлеров
setup_handlers(dp)


async def on_startup():
    await init_pool()
    await create_table()
    logger.info('Бот запущен и готов к работе.')


async def main():
    await on_startup()
    await dp.start_polling(
        bot,
        allowed_updates=[
            UpdateType.MESSAGE,
            UpdateType.EDITED_MESSAGE,
            UpdateType.CALLBACK_QUERY,
            UpdateType.MY_CHAT_MEMBER,
            UpdateType.CHAT_MEMBER,
        ]
    )


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info('Бот остановлен.') 