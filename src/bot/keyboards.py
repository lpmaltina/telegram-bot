from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="🔎 🔎 🔎 Посмотреть все тексты", callback_data="get_all_reviews")
    kb.button(text="🔎 Посмотреть один текст", callback_data="get_one_review")
    kb.button(text="📝 Добавить текст", callback_data="add_review")
    kb.button(text="✍️ Отредактировать текст", callback_data="edit_review")
    kb.button(text="❌ Удалить один текст", callback_data="delete_one_review")
    kb.button(text="❌ ❌ ❌ Удалить все тексты", callback_data="delete_all_reviews")
    kb.adjust(1)
    return kb.as_markup()
