import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
from aiogram.utils import executor
import hashlib
import os

logging.basicConfig(level=logging.INFO)

# 🔑 Сюда вставь токен от BotFather
API_TOKEN = "8195703213:AAF792v5vuBt7LBho5feo1NlJEYpitIcKqM"


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# 📒 Словарь "короткая команда -> заметка"
NOTES = {
    "привет": "Привет! 👋 Это заметка.",
    "ссылки": "Полезные ссылки:\nhttps://example.com",
    "дела": "Список дел:\n- Купить хлеб\n- Сделать бота"
}

# обработка inline-запроса
@dp.inline_handler()
async def inline_echo(inline_query: types.InlineQuery):
    text = inline_query.query.strip().lower()
    results = []

    if text in NOTES:
        note = NOTES[text]
        results.append(
            InlineQueryResultArticle(
                id=hashlib.md5(text.encode()).hexdigest(),
                title=f"Заметка: {text}",
                input_message_content=InputTextMessageContent(note),
                description=note[:50]  # короткое описание
            )
        )
    elif text:  # если ввели что-то, но нет заметки
        results.append(
            InlineQueryResultArticle(
                id=hashlib.md5(text.encode()).hexdigest(),
                title="Нет такой заметки",
                input_message_content=InputTextMessageContent("❌ Заметка не найдена")
            )
        )

    await inline_query.answer(results, cache_time=1)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
