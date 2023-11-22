from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

reply_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Рейтинг📄")]], resize_keyboard=True)


def get_reply_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()

    keyboard_builder.button(text="Рейтинг📄")
    return keyboard_builder.as_markup(resize_keyboard=True)
