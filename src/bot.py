import asyncio

from aiogram.client.default import DefaultBotProperties

from handlers import register_handlers

from aiogram import Dispatcher, Bot
from aiogram.utils.i18n import I18n
from aiogram.fsm.storage.memory import MemoryStorage

# from aiogram.utils.i18n.middleware import ConstI18nMiddleware

from pathlib import Path
from loguru import logger
from dotenv import load_dotenv

from models.db_gino import connect_to_db


async def main() -> None:
    base_dir = Path(__file__).resolve().parent.parent

    load_dotenv(base_dir / '.env')
    logger.add(base_dir / 'logs.log', level="INFO")

    import config

    bot = Bot(config.BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher(storage=MemoryStorage(), bot=bot)
    # i18n = I18n(path='locales', default_locale='ru')
    # dp.message.middleware(ConstI18nMiddleware('ru', i18n))

    register_handlers(dp)

    loop = asyncio.get_event_loop()
    loop.create_task(connect_to_db())

    logger.info('Bot started')

    await dp.start_polling(bot)

    logger.info('Bot stopped')


if __name__ == '__main__':
    asyncio.run(main())
