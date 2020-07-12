import telebot
import asyncio
from datetime import datetime
from secrets import token, goldname
from data import Point


class AsyncBot(telebot.TeleBot):
    async def async_polling(self):
        while True:
            self.update_messages()
            await asyncio.sleep(1)

    def update_messages(self):
        """
        Retrieves any updates from the Telegram API.
        Registered listeners and applicable message handlers will be notified when a new message arrives.
        :raises ApiException when a call has failed.
        """
        updates = self.get_updates(offset=(self.last_update_id + 1), timeout=1)
        self.process_new_updates(updates)


bot = AsyncBot(token, threaded=False)


def validate_user(func):
    def f(message):
        if message.from_user.username != goldname:
            bot.send_message(message.chat.id, "Вам нельзя")
            return
        return func(message)
    return f


@bot.message_handler(commands=["start"])
@validate_user
def start_message(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Привет")


@bot.message_handler(commands=["remove_last"])
@validate_user
def remove_last_point(message: telebot.types.Message):
    if not len(Point.select()):
        bot.send_message(message.chat.id, "Нет точек")
        return
    point = Point.select().order_by(Point.date.desc()).get()
    if point:
        point.delete_instance()
        bot.send_message(message.chat.id, "Последняя точка удалена")


@bot.message_handler(commands=["break_line"])
@validate_user
def break_line(message: telebot.types.Message):
    if not len(Point.select()):
        bot.send_message(message.chat.id, "Нет точек")
        return
    point = Point.select().order_by(Point.date.desc()).get()
    if point:
        point.is_newline = True
        point.save()
        bot.send_message(message.chat.id, "Линия прервана")


@bot.message_handler(content_types="location")
@validate_user
def receive_point(message: telebot.types.Message):
    point = Point(date=datetime.fromtimestamp(message.date), x=message.location.latitude, y=message.location.longitude,
                  comment=str(datetime.fromtimestamp(message.date)))
    point.save()
    bot.send_message(message.chat.id, "Сохранено")
