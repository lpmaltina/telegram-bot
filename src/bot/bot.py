import asyncio
import logging
import os

import requests
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from dotenv import load_dotenv

from src.bot.keyboards import main_keyboard
from src.mistral import get_mistral_answer

BOT_URL = "http://127.0.0.1:8000"

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
bot = Bot(BOT_TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)


@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.reply(
        "Добро пожаловать!",
        reply_markup=main_keyboard()
    )


@dp.callback_query(F.data == "get_all_reviews")
async def get_all_reviews(callback: types.CallbackQuery):
    response = requests.get(f"{BOT_URL}/get_all/")
    await callback.message.answer(response.text)


@dp.callback_query(F.data == "get_one_review")
async def get_one_review(callback: types.CallbackQuery):
    await callback.message.answer("Чтобы посмотреть один текст, используйте команду /get_by_id <id текста>")
    await callback.answer()


@dp.message(Command("get_by_id"))
async def get_by_id(message: types.Message):
    _, review_id = message.text.split()
    review_id = int(review_id)
    response = requests.get(f"{BOT_URL}/get_by_id?data_id={review_id}")
    await message.reply(response.text)


@dp.callback_query(F.data == "add_review")
async def add_review(callback: types.CallbackQuery):
    await callback.message.answer("Чтобы добавить текст, используйте команду /add <текст>")
    await callback.answer()


@dp.message(Command("add"))
async def add_review(message: types.Message):
    _, text = message.text.split(maxsplit=1)
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    response = requests.post(f"{BOT_URL}/add/", headers=headers, json={"review": text})
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


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
