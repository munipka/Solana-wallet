import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from handlers.commands import register_commands
from handlers.callbacks import register_callbacks
from handlers.SendRegister import register_state_callbacks

import config
from database import create_tables

bot = Bot(token=config.BOT_TOKEN)


async def main():
    dp = Dispatcher(bot, storage=MemoryStorage())
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    await create_tables()  # creates tables in DB
    register_commands(dp)
    register_callbacks(dp)
    register_state_callbacks(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
