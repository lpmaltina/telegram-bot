import os

import aiosqlite
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

START_TEXT = "Добро пожаловать!"
DB_PATH = os.path.join("../data", "texts.db")
router = Router()


@router.message(Command("start"))
async def start_handler(message: Message) -> None:
    await message.answer(START_TEXT)


@router.message(Command("get_text"))
async def get_text_handler(message: Message) -> None:
    command = message.text.split()
    _, id_text = command
    conn = await aiosqlite.connect(DB_PATH)
    cursor = await conn.execute(
        """SELECT text
        FROM Texts
        WHERE id_text = ?""",
        (id_text,)
    )
    text = await cursor.fetchone()
    await cursor.close()
    await conn.close()
    await message.answer(text[0])
