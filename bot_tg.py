import telebot
from telebot import types
import requests
import re
import os
from api.config.config import API_URL
from dotenv import load_dotenv

load_dotenv("api\config\.env")
bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
bottom_main = types.KeyboardButton("Рейтинг📄")

markup.row(bottom_main)


@bot.message_handler(commands=["start"])
def main(message):
    bot.send_message(
        message.chat.id,
        "Привет! Этот бот нужен чтобы узнать свой рейтинг, для этого введите снилс",
        reply_markup=markup,
    )


@bot.message_handler(content_types=["text"])
def func(message):
    if message.text == "Рейтинг📄":
        bot.send_message(message.chat.id, "Введите снилс целиком без разделителей ")
        bot.register_next_step_handler(message, get_rating)


def get_rating(message):
    reg = "^\d{11}$"
    match_ = re.search(reg, message.text)
    if match_ is not None:
        a = requests.get(f"{API_URL}{message.text}")
        if a.json() == []:
            bot.reply_to(message, "Данный снилс отсутствует в базе")
        else:
            answer = f"Баллы: {a.json()[0]['points_fin']}\n\n"
            for i in a.json():
                answer += f"{i['direction']}: {i['rating']} место\n\n"
            bot.reply_to(message, answer)
    else:
        bot.reply_to(message, "Неверно введен снилс")


bot.polling(non_stop=True)
