from aiogram import Bot
from aiogram.types import (
    Message,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    input_text_message_content,
)
from bot_core.keyboards.keyboard import reply_keyboard, get_reply_keyboard
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import re
import requests
from api.config.config import API_URL
import hashlib


class BotState(StatesGroup):
    normal_state = State()
    check_snils = State()


async def get_start(message: Message, bot: Bot):
    await message.answer(
        "Привет! Этот бот нужен чтобы узнать свой рейтинг, для этого введите снилс", reply_markup=get_reply_keyboard()
    )


async def null_answer(message: Message, bot: Bot):
    await message.answer("Мне не знакома эта команда")


async def get_rating(message: Message, bot: Bot, state: FSMContext):
    await message.answer("Введите снилс целиком без разделителей")
    await state.set_state(BotState.check_snils)


async def back_answer_about_rating(message: Message, bot: Bot, state: FSMContext):
    reg = "^\d{11}$"
    match_ = re.search(reg, message.text)
    if match_ is not None:
        a = requests.get(f"{API_URL}{message.text}")
        if a.json() == []:
            await message.answer("Данный снилс отсутствует в базе")
        else:
            answer = f"Баллы: {a.json()[0]['points_fin']}\n\n"
            for i in a.json():
                answer += f"{i['direction']}: {i['rating']} место\n\n"
            await message.answer(answer)
    else:
        await message.answer("Неверно введен снилс")

    await state.set_state(BotState.normal_state)


def back_answer_about_rating_to_text(message: str):
    reg = "^\d{11}$"
    match_ = re.search(reg, message)
    if match_ is not None:
        a = requests.get(f"{API_URL}{message}")
        if a.json() == []:
            return "Данный снилс отсутствует в базе"
        else:
            answer = f"Баллы: {a.json()[0]['points_fin']}\n\n"
            for i in a.json():
                answer += f"{i['direction']}: {i['rating']} место\n\n"
            return answer
    else:
        return "Неверно введен снилс"


async def inline_back_answer_about_rating(inline_query: InlineQuery, bot: Bot) -> None:
    text = back_answer_about_rating_to_text(inline_query.query or "null")
    input_content = InputTextMessageContent(message_text=text)
    result_id = hashlib.md5(text.encode()).hexdigest()
    item = InlineQueryResultArticle(
        input_message_content=input_content, id=result_id, title="Введите снилс целиком без разделителей"
    )

    await bot.answer_inline_query(inline_query_id=inline_query.id, results=[item], cache_time=1)
