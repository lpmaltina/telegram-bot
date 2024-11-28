import asyncio
import json
import logging
import os

import requests
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from dotenv import load_dotenv

from src.mistral import get_mistral_answer

WELCOME_MESSAGE = "Добро пожаловать!"
REQUEST_ERROR = "Не удалось выполнить запрос!"
WRONG_COMMAND = "Неправильный формат команды!"
ID_IS_NOT_INT = "id должен быть целым числом!"
UNKNOWN_COMMAND = "Неизвестная команда!"

BOT_URL = "http://127.0.0.1:8000"

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
bot = Bot(BOT_TOKEN)
dp = Dispatcher()

HEADERS = {
    "accept": "application/json",
    "Content-Type": "application/json"
}
logging.basicConfig(level=logging.INFO)


def stringify_response(response):
    return json.dumps(response.json(), ensure_ascii=False, indent=4)


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.reply(WELCOME_MESSAGE)


@dp.message(Command("get_all"))
async def get_all(message: types.Message):
    try:
        response = requests.get(f"{BOT_URL}/get_all")
        answer = stringify_response(response)
    except:
        answer = REQUEST_ERROR
    await message.reply(answer)


@dp.message(Command("get_by_id"))
async def get_by_id(message: types.Message):
    tokens = message.text.split()
    if len(tokens) == 2:
        try:
            review_id = int(tokens[1])
            try:
                response = requests.get(f"{BOT_URL}/get/{review_id}")
                answer = stringify_response(response)
            except:
                answer = REQUEST_ERROR
        except ValueError:
            answer = ID_IS_NOT_INT
    else:
        answer = WRONG_COMMAND
    await message.reply(answer)


@dp.message(Command("edit"))
async def get_by_id(message: types.Message):
    try:
        _, review_id, review = message.text.split(maxsplit=2)
        try:
            review_id = int(review_id)
            try:
                response = requests.put(
                    f"{BOT_URL}/edit/",
                    headers=HEADERS,
                    json={"id": review_id, "review": review}
                )
                answer = stringify_response(response)
            except:
                answer = REQUEST_ERROR
        except ValueError:
            answer = ID_IS_NOT_INT
    except:
        answer = WRONG_COMMAND
    await message.reply(answer)


@dp.message(Command("add"))
async def add(message: types.Message):
    try:
        _, review = message.text.split(maxsplit=1)
        try:
            response = requests.post(
                f"{BOT_URL}/add", headers=HEADERS, json={"review": review}
            )
            answer = stringify_response(response)
        except:
            answer = REQUEST_ERROR
    except:
         answer = WRONG_COMMAND
    await message.reply(answer)


@dp.message(Command("delete_by_id"))
async def delete_by_id(message: types.Message):
    tokens = message.text.split()
    if len(tokens) == 2:
        try:
            review_id = int(tokens[1])
            try:
                response = requests.delete(f"{BOT_URL}/delete/{review_id}")
                answer = stringify_response(response)
            except:
                answer = REQUEST_ERROR
        except ValueError:
            answer = ID_IS_NOT_INT
    else:
        answer = WRONG_COMMAND
    await message.reply(answer)


@dp.message(Command("delete_all"))
async def delete_all(message: types.Message):
    try:
        response = requests.delete(f"{BOT_URL}/delete_all")
        answer = stringify_response(response)
    except:
        answer = REQUEST_ERROR
    await message.reply(answer)


@dp.message(Command("sentiment"))
async def sentiment(message: types.Message):
    pass
#     prompt = f"""Determine the sentiment of the following text. Only respond with the exact words "positive" or "negative".
#
# {message.text}"""
#     mistral_answer = await get_mistral_answer(prompt)
#     await message.reply(mistral_answer)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
