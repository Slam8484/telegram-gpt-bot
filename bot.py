import os
import asyncio
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.filters import CommandStart
from dotenv import load_dotenv
import openai

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет! 👋 Я GPT-бот. Напиши мне что-нибудь, и я отвечу!")

@router.message()
async def handle_message(message: Message):
    try:
        print("Пользователь:", message.text)

        response = openai.ChatCompletion.create(
            model="mistralai/Mistral-7B-Instruct-v0.2",
            messages=[{"role": "user", "content": message.text}]
        )

        reply_text = response["choices"][0]["message"]["content"]
        print("Ответ GPT:", reply_text)
        await message.answer(reply_text)

    except Exception as e:
        print("Ошибка:", e)
        await message.answer("⚠️ Ошибка при обработке запроса.")

async def main():
    bot = Bot(token=TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


