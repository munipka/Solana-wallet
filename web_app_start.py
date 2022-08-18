import aiohttp
from aiogram import Bot
import config

from aiohttp import web
from webApp.web_app import routes as webapp_routes

bot = Bot(config.BOT_TOKEN)


async def webapp():
    app = web.Application()
    app["bot"] = bot
    app.add_routes(webapp_routes)
    app.router.add_static(prefix='/static', path='static')

    return app


if __name__ == "__main__":
    aiohttp.web.run_app(webapp(), port=8001, host="65.108.147.234")
