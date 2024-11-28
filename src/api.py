from fastapi import FastAPI
from starlette.responses import JSONResponse

from src.database.dao import ReviewDAO
from src.database.schemas import SReviewAdd, SReviewUpdate

app = FastAPI()


@app.get("/get_all", tags=["Тексты"], summary="Получить все тексты")
async def get_all() -> JSONResponse:
    reviews = await ReviewDAO.find_all()
    if reviews:
        return JSONResponse(
        {
            "message": "Тексты успешно найдены!",
            "reviews": [review.to_dict() for review in reviews]
        },
        status_code=200
    )
    return JSONResponse(
            {"message": "Текстов не найдено!"},
            status_code=404
        )


@app.get("/get/{data_id}", tags=["Тексты"], summary="Получить текст по id")
async def get_by_id(data_id: int) -> JSONResponse:
    review = await ReviewDAO.find_by_id(data_id=data_id)
    if review is not None:
        return JSONResponse(
        {
            "message": f"Текст с ID={data_id} успешно найден!",
            "review": review.review
        },
        status_code=200
    )
    return JSONResponse(
        {"message": f"Текст с ID={data_id} не найден!"},
        status_code=404
    )


@app.post("/add", tags=["Тексты"], summary="Добавить текст")
async def add(review: SReviewAdd):
    check = await ReviewDAO.add(**review.dict())
    if check:
        return JSONResponse(
            {"message": "Текст успешно добавлен!", "review": review.review},
            status_code=200
        )
    return JSONResponse(
        {"message": "Ошибка при добавлении текста!"},
        status_code=404
    )


@app.put("/edit", tags=["Тексты"], summary="Редактировать текст по id")
async def edit(review: SReviewUpdate) -> JSONResponse:
    check = await ReviewDAO.update(filter_by={"id": review.id}, review=review.review)
    if check:
        return JSONResponse(
            {"message": f"Текст с ID={review.id} изменён!"},
            status_code=200
        )
    return JSONResponse(
        {"message": "Ошибка при редактировании текста!"},
        status_code=404
    )


@app.delete("/delete/{data_id}", tags=["Тексты"], summary="Удалить текст по id")
async def delete_review(data_id: int) -> JSONResponse:
    check = await ReviewDAO.delete(id=data_id)
    if check:
        return JSONResponse(
            {"message": f"Текст с ID={data_id} удалён!"},
            status_code=200
        )
    return JSONResponse(
        {"message": "Ошибка при удалении данных!"},
        status_code=404
    )


@app.delete("/delete_all", tags=["Тексты"], summary="Удалить все тексты")
async def delete_all() -> JSONResponse:
    check = await ReviewDAO.delete(delete_all=True)
    if check:
        return JSONResponse(
            {"message": "Все данные удалены!"},
            status_code=200
        )
    return JSONResponse(
        {"message": "Ошибка при удалении данных!"},
        status_code=404
    )
