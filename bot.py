import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
import openai

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

router = Router()

@router.message(commands=["start"])
async def cmd_start(message: Message):
    await message.answer("Привет! Я GPT-бот. Напиши мне что-нибудь, и я постараюсь ответить!")

@router.message()
async def handle_message(message: Message):
    try:
        print("Пользователь:", message.text)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}]
        )
        reply_text = response["choices"][0]["message"]["content"]
        print("Ответ GPT:", reply_text)
        await message.answer(reply_text)
    except Exception as e:
        print("Ошибка:", e)
        await message.answer("⚠️ Ошибка при обработке запроса.")

async def main():
    bot = Bot(
        token=TELEGRAM_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

