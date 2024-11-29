import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
from src.bot import bot_requests, utils


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(BOT_TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)


@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.reply(utils.WELCOME_MESSAGE + "\n\n" + utils.HELP_MESSAGE)


@dp.message(Command("help"))
async def help_cmd(message: types.Message):
    await message.reply(utils.HELP_MESSAGE)


@dp.message(Command("get_all"))
async def get_all_cmd(message: types.Message):
    answer = await bot_requests.get_all_request()
    await message.reply(answer)


@dp.message(Command("get_by_id"))
async def get_by_id_cmd(message: types.Message):
    tokens = message.text.split()
    if len(tokens) == 2:
        try:
            review_id = int(tokens[1])
            answer = await bot_requests.get_by_id_request(review_id)
        except ValueError:
            answer = utils.ID_IS_NOT_INT
    else:
        answer = utils.WRONG_COMMAND
    await message.reply(answer)


@dp.message(Command("edit"))
async def edit_by_id_cmd(message: types.Message):
    try:
        _, review_id, review = message.text.split(maxsplit=2)
        try:
            review_id = int(review_id)
            answer = await bot_requests.edit_by_id_request(review_id, review)
        except ValueError:
            answer = utils.ID_IS_NOT_INT
    except:
        answer = utils.WRONG_COMMAND
    await message.reply(answer)


@dp.message(Command("add"))
async def add_cmd(message: types.Message):
    try:
        _, review = message.text.split(maxsplit=1)
        answer = await bot_requests.add_request(review)
    except:
         answer = utils.WRONG_COMMAND
    await message.reply(answer)


@dp.message(Command("delete_by_id"))
async def delete_by_id_cmd(message: types.Message):
    tokens = message.text.split()
    if len(tokens) == 2:
        try:
            review_id = int(tokens[1])
            answer = await bot_requests(review_id)
        except ValueError:
            answer = utils.ID_IS_NOT_INT
    else:
        answer = utils.WRONG_COMMAND
    await message.reply(answer)


@dp.message(Command("delete_all"))
async def delete_all_cmd(message: types.Message):
    answer = bot_requests.delete_all_request()
    await message.reply(answer)


@dp.message(Command("sentiment"))
async def sentiment_cmd(message: types.Message):
    try:
        _, review = message.text.split(maxsplit=1)
        answer = bot_requests.sentiment_request(review)
    except:
        answer = utils.WRONG_COMMAND
    await message.reply(answer)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
