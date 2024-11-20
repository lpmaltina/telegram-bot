import sqlite3
import os

import telebot

from tg_token import TELEGRAM_TOKEN

bot = telebot.TeleBot(TELEGRAM_TOKEN)
START_TEXT = """Добро пожаловать!
Чтобы получить текст по id, используйте команду /get_text <id>.
id должен быть целым числом."""
DB_PATH = os.path.join("data", "texts.db")


@bot.message_handler(commands=["start"])
def show_start_message(message):
    bot.send_message(message.from_user.id, START_TEXT)


def get_id_from_message(message):
    command = message.text.split()
    _, id_text = command
    return id_text


@bot.message_handler(commands=["get_text"])
def get_text_by_id(message):
    id_text = get_id_from_message(message)
    conn = sqlite3.connect(DB_PATH)
    with conn:
        cursor = conn.execute(
            """SELECT text
            FROM Texts
            WHERE id_text = ?""",
            (id_text,)
        )
        text = cursor.fetchone()[0]
    bot.send_message(message.from_user.id, text)


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True, interval=0)
        except Exception as e:
            print(e)