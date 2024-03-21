import asyncio
from aiogram import Bot, Dispatcher
import logging
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import common, setuping_workout
from config_reader import config


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(common.router, setuping_workout.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
