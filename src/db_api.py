import os

import aiosqlite
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
DB_PATH = os.path.join("..", "data", "texts.db")
app = FastAPI()

@app.get(
    "/get_text",
    summary="Получение текста по ID"
)
async def get_text_by_id(
        id_text: int = Query(
            ...,
            description="Уникальный идентификатор текста"
        )
    ):
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
    if text is None:
        return JSONResponse(
            {"message": "Ошибка: текста с данным ID не найдено"},
            status_code=404
        )
    return JSONResponse({"text": text[0]}, status_code=200)
