import os
import asyncio
import openai
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.filters import CommandStart

# Загружаем переменные из .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Настройка OpenAI через DeepInfra
openai.api_key = OPENAI_API_KEY
openai.api_base = "https://api.deepinfra.com/v1/openai"

# Память диалогов: user_id -> list of messages
chat_history = {}

# Настройка бота
bot = Bot(
    token=TELEGRAM_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("👋 Привет! Я GPT-бот через DeepInfra. Напиши что-нибудь, и я постараюсь помочь.")
    chat_history[message.from_user.id] = []  # сбрасываем историю

@router.message()
async def handle_message(message: Message):
    user_id = message.from_user.id
    user_input = message.text

    print(f"Пользователь ({user_id}):", user_input)

    # Подготовка истории
    if user_id not in chat_history:
        chat_history[user_id] = []

    chat_history[user_id].append({"role": "user", "content": user_input})

    # Обрезаем историю (последние 10 сообщений)
    recent_history = chat_history[user_id][-10:]

    try:
        response = openai.ChatCompletion.create(
            model="mistralai/Mistral-7B-Instruct-v0.2",
            messages=recent_history
        )
        reply_text = response["choices"][0]["message"]["content"]
        chat_history[user_id].append({"role": "assistant", "content": reply_text})
        print("Ответ GPT:", reply_text)
        await message.answer(reply_text)
    except Exception as e:
        print("❌ Ошибка:", e)
        await message.answer("⚠️ Ошибка при обращении к GPT-прокси.")

async def main():
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


