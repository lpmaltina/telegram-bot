import os

import aiosqlite
from fastapi import FastAPI

DB_PATH = os.path.join("..", "data", "texts.db")
app = FastAPI()

@app.get("/get_text/{id_text}")
async def get_text_by_id(id_text: int) -> str:
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
    return text[0]
