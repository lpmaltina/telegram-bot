import asyncio
import os
import logging

import requests
from aiogram.filters import Command
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import BotCommand, BotCommandScopeDefault

from mistral import get_mistral_answer

BOT_URL = "http://127.0.0.1:8000"

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
bot = Bot(BOT_TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.reply("Добро пожаловать!")

@dp.message(Command("reviews"))
async def get_reviews(message: types.Message):
    response = requests.get(f"{BOT_URL}/reviews/")
    await message.reply(response.text)

@dp.message(Command("review"))
async def get_review(message: types.Message):
    _, review_id = message.text.split()
    review_id = int(review_id)
    response = requests.get(f"{BOT_URL}/review?data_id={review_id}")
    await message.reply(response.text)


@dp.message(Command("add"))
async def add_review(message: types.Message):
    _, text = message.text.split(maxsplit=1)
    headers = {
        "accept': 'application/json",
        "Content-Type': 'application/json"
    }
    response = requests.post(f"{BOT_URL}/add_review", headers=headers, json={"review": text})
    await message.reply(response.text)

@dp.message(F.text)
async def chat_with_mistral(message: types.Message):
    pass
#     prompt = f"""Determine the sentiment of the following text. Only respond with the exact words "positive" or "negative".
#
# {message.text}"""
#     mistral_answer = await get_mistral_answer(prompt)
#     await message.reply(mistral_answer)

# async def start_bot():
#     try:
#         await bot.send_message(ADMIN_ID, "Бот запущен")
#     except:
#         pass
#
#
# async def stop_bot():
#     try:
#         await bot.send_message(ADMIN_ID, "Бот остановлен")
#     except:
#         pass

async def set_commands():
    commands = [
        BotCommand(command="start", description="Старт"),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
