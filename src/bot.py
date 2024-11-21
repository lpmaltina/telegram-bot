import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

import db_api
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
START_TEXT = """Добро пожаловать!
Чтобы получить текст по id, используйте команду /get_text <id>.
id должен быть целым числом."""
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


def get_id_from_message(message):
    command = message.text.split()
    _, id_text = command
    return id_text


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(START_TEXT)


@dp.message(Command("get_text"))
async def get_text_by_id(message):
    id_text = get_id_from_message(message)
    text = await db_api.get_text_by_id(id_text)
    await message.answer(text)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
