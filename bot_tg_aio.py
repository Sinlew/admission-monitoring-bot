from aiogram import Bot, Dispatcher, F
import asyncio
import os
from api.config.config import API_URL
from dotenv import load_dotenv
import logging
from bot_core.handler.basic import (
    get_start,
    get_rating,
    null_answer,
    BotState,
    back_answer_about_rating,
    inline_back_answer_about_rating,
)
from aiogram.filters import Command

from bot_core.keyboards.keyboard import reply_keyboard


load_dotenv("api\config\.env")
bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))

dp = Dispatcher()


async def start_bot():
    await bot.send_message(os.getenv("ADMIN_ID"), "bot is starting")


async def start():
    await bot.delete_webhook(drop_pending_updates=True)
    logging.basicConfig(level=logging.INFO)
    dp.startup.register(start_bot)
    dp.message.register(get_start, Command(commands=["start"]))
    dp.message.register(get_rating, F.text == "Рейтинг📄")
    dp.message.register(back_answer_about_rating, BotState.check_snils)
    dp.message.register(null_answer, lambda msg: msg.text)
    dp.inline_query.register(inline_back_answer_about_rating)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
