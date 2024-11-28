import asyncio
import json
import logging
import os

import httpx
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
from starlette.responses import JSONResponse

from src.mistral import get_mistral_answer

WELCOME_MESSAGE = "Добро пожаловать!"
REQUEST_ERROR = "Не удалось выполнить запрос!"
WRONG_COMMAND = "Неправильный формат команды!"
ID_IS_NOT_INT = "id должен быть целым числом!"
UNKNOWN_COMMAND = "Неизвестная команда!"

URL = "http://127.0.0.1:8000"

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(BOT_TOKEN)
dp = Dispatcher()

HEADERS = {
    "accept": "application/json",
    "Content-Type": "application/json"
}
logging.basicConfig(level=logging.INFO)


def stringify_response(response) -> str:
    return json.dumps(response.json(), ensure_ascii=False, indent=4)


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.reply(WELCOME_MESSAGE)


@dp.message(Command("get_all"))
async def get_all(message: types.Message):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{URL}/get_all")
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
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"{URL}/get/{review_id}")
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
                async with httpx.AsyncClient() as client:
                    response = await client.put(
                        f"{URL}/edit",
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
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{URL}/add", headers=HEADERS, json={"review": review}
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
                async with httpx.AsyncClient() as client:
                    response = await client.delete(f"{URL}/delete/{review_id}")
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
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{URL}/delete_all")
        answer = stringify_response(response)
    except:
        answer = REQUEST_ERROR
    await message.reply(answer)


@dp.message(Command("sentiment"))
async def sentiment(message: types.Message):
    try:
        _, review = message.text.split(maxsplit=1)
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{URL}/sentiment/{review}")
            answer = stringify_response(response)
        except:
            answer = REQUEST_ERROR
    except:
        answer = WRONG_COMMAND
    await message.reply(answer)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
