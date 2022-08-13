import aiohttp
from aiogram import Bot, Dispatcher


from aiohttp import web
from webApp.web_app import routes as webapp_routes
from webApp.web_app import setup_template_routes

bot = Bot(token="5127938226:AAHrJTQ-Nei47CWYgKGIChtfk9J8mxy4KC0")


async def webapp():
    app = web.Application()
    app["bot"] = bot
    app.add_routes(webapp_routes)
    app.router.add_static(prefix='/static', path='static')
    setup_template_routes(app)

    return app


if __name__ == "__main__":
    aiohttp.web.run_app(webapp(), port=8000, host="localhost")
