from fastapi import FastAPI

from src.database.dao import ReviewDAO
from src.database.schemas import SReviewAdd, SReviewUpdate

app = FastAPI()


@app.get("/get_all", tags=["Тексты"], summary="Получить все тексты")
async def get_all_reviews():
    reviews = await ReviewDAO.find_all()
    if not reviews:
        return {"message": "Текстов не найдено!"}
    return reviews


@app.get("/get/{data_id}", tags=["Тексты"], summary="Получить текст по id")
async def get_review(data_id: int):
    review = await ReviewDAO.find_by_id(data_id=data_id)
    if review is None:
        return {"message": f"Текст с ID={data_id} не найден!"}
    return review.review


@app.post("/add", tags=["Тексты"], summary="Добавить текст")
async def add_review(review: SReviewAdd):
    check = await ReviewDAO.add(**review.dict())
    if check:
        return {"message": "Текст успешно добавлен!", "review": review.review}
    return {"message": "Ошибка при добавлении текста!"}


@app.put("/edit", tags=["Тексты"], summary="Редактировать текст по id")
async def edit_review(review: SReviewUpdate) -> dict:
    check = await ReviewDAO.update(filter_by={"id": review.id}, review=review.review)
    if check:
        return {"message": f"Текст с ID={review.id} изменён!"}
    return {"message": "Ошибка при редактировании текста!"}


@app.delete("/delete/{data_id}", tags=["Тексты"], summary="Удалить текст по id")
async def delete_review(data_id: int) -> dict:
    check = await ReviewDAO.delete(id=data_id)
    if check:
        return {"message": f"Текст с ID={data_id} удалён!"}
    return {"message": "Ошибка при удалении данных!"}


@app.delete("/delete_all", tags=["Тексты"], summary="Удалить все тексты")
async def delete_all() -> dict:
    check = await ReviewDAO.delete(delete_all=True)
    if check:
        return {"message": "Все данные удалены!"}
    return {"message": "Ошибка при удалении данных!"}
