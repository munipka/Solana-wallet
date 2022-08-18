import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from handlersTEst.commands import register_commands
from handlersTEst.callbacks import register_callbacks
from handlersTEst.SendRegister import register_state_callbacks

from aiohttp import web
from webApp.web_app import routes as webapp_routes
from webApp.web_app import setup_template_routes

import config
from database import create_tables

bot = Bot(token=config.BOT_TOKEN)




async def main():
    dp = Dispatcher(bot, storage=MemoryStorage())
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    create_tables() #creates tables in DB
    register_commands(dp)
    register_callbacks(dp)
    register_state_callbacks(dp)
    
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())
