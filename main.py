import asyncio
from asyncbot import bot
from webserver import WebServer
from data import Point

server = WebServer()


if __name__ == '__main__':

    # Create database if not exists
    Point.create_table()

    loop = asyncio.get_event_loop()
    loop.create_task(server.run())
    loop.create_task(bot.async_polling())
    loop.run_forever()
