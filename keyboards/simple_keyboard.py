from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def make_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for i in items:
        builder.add(KeyboardButton(text=str(i)))
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=True)
