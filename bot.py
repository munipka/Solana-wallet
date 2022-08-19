import asyncio
import logging
from asyncio import create_task

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from handlers.commands import register_commands
from handlers.callbacks import register_callbacks
from handlers.SendRegister import register_state_callbacks

import config
from apps.database import create_tables
from apps.notifications import notifications

bot = Bot(token=config.BOT_TOKEN)


async def m():
    dp = Dispatcher(bot, storage=MemoryStorage())
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    register_commands(dp)
    register_callbacks(dp)
    register_state_callbacks(dp)

    await create_tables()  # creates tables in DB

    await dp.start_polling(bot)


async def notf(bot):
    await notifications(bot)


async def main():
    f1 = create_task(m())
    f2 = create_task(notf(bot))
    await asyncio.wait([f1, f2])


if __name__ == "__main__":
    asyncio.run(main())
