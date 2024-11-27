# Telegram Bot

**Стек**:
- sqlalchemy
- FastAPI
- aiogram

## База данных

### Таблицы:
- #### reviews

    **Столбцы**:
    - *id* - id текста
    - *review* - текст
  
## FastAPI

- **/get_all** - получить все тексты
- **/get/{data_id}** - получить текст по id
- **/add** - добавить текст
- **/edit** - редактировать текст по id
- **/delete/{data_id}** - удалить текст по id
- **/delete_all** - удалить все тексты

Команда для запуска FastAPI:
$ uvicorn src.api:app --reload

Файл с кодом, который нужно запустить для запуска telegram-бота:
src/bot/bot.py
