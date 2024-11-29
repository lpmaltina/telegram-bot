# Telegram Bot

Telegram-бот позволяет взаимодействовать через API с базой данных (просматривать данные, добавлять, изменять и удалять их) и с большой языковой моделью (open-mistral-nemo).

**Стек**:
- http-запросы: **httpx**
- СУБД: **SQLite**
- ORM: **sqlalchemy**
- создание API: **FastAPI**
- создание telegram-бота: **aiogram**
- анализ тональности: **LLM (open-mistral-nemo)**

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
- **/sentiment/{text}** - получить результат анализа тональности текста: positive или negative

## Telegram-бот

**Команды**:
- **/start** - отобразить приветственное сообщение и список команд
- **/help** - отобразить список команд
- **/get_all** - получить все тексты
- **/get_by_id <id текста>** - получить текст по id
- **/add <текст>** - добавить текст
- **/edit <id текста> <отредактированный текст>** - редактировать текст по id
- **/delete_by_id <id>** - удалить текст по id
- **/delete_all** - удалить все тексты
- **/sentiment <текст>** - получить результат анализа тональности текста: positive или negative

## Как использовать

1) запустить команду

$ uvicorn src.api:app --reload

2) выполнить код из файла src/bot/bot.py
