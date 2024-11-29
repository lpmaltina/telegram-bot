import json


WELCOME_MESSAGE = "Добро пожаловать!"
REQUEST_ERROR = "Не удалось выполнить запрос!"
WRONG_COMMAND = "Неправильный формат команды!"
ID_IS_NOT_INT = "id должен быть целым числом!"
UNKNOWN_COMMAND = "Неизвестная команда!"

HELP_MESSAGE = """Список команд:

/start - отобразить приветственное сообщение и список команд

/help - отобразить список команд

/get_all - получить все тексты

/get_by_id <id текста> - получить текст по id

/add <текст> - добавить текст

/edit <id текста> <отредактированный текст> - редактировать текст по id

/delete_by_id <id> - удалить текст по id

/delete_all - удалить все тексты

/sentiment <текст> - получить результат анализа тональности текста: positive или negative"""


def stringify_response(response) -> str:
    return json.dumps(response.json(), ensure_ascii=False, indent=4)
