from fastapi import FastAPI

from dao import ReviewDAO
from schemas import SReviewAdd


app = FastAPI()


@app.get("/reviews/", summary="Получить все тексты")
async def get_reviews():
    reviews = await ReviewDAO.find_all()
    if not reviews:
        return {"message": "Текстов не найдено!"}
    return reviews


@app.get("/review/", summary="Получить текст по id")
async def get_review(data_id: int):
    review = await ReviewDAO.find_by_id(data_id=data_id)
    if review is None:
        return {"message": f"Текст с ID={data_id} не найден!"}
    return review.review


@app.post("/add_review/", summary="Добавить текст")
async def add_review(review: SReviewAdd):
    check = await ReviewDAO.add(**review.dict())
    if check:
        return {"message": "Текст успешно добавлен!", "review": review.review}
    return {"message": "Ошибка при добавлении текста!"}


@app.post("/add_review/", summary="Добавить текст")
async def add_review(review: SReviewAdd):
    check = await ReviewDAO.add(**review.dict())
    if check:
        return {"message": "Текст успешно добавлен!", "review": review.review}
    return {"message": "Ошибка при добавлении текста!"}


@app.delete("/clear/", summary="Удалить все тексты")
async def delete_all() -> dict:
    check = await ReviewDAO.delete(delete_all=True)
    if check:
        return {"message": "Все данные удалены!"}
    return {"message": "Ошибка при удалении данных!"}
