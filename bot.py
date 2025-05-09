import os
import openai
from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv

# Загружаем токены из .env файла
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Настройка OpenAI
openai.api_base = "https://api.deepinfra.com/v1/openai"
openai.api_key = OPENAI_API_KEY

# Инициализация Telegram бота
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("👋 Привет, Вячеслав!\nЯ бот на базе GPT. Напиши мне любой вопрос, и я постараюсь помочь!")

@dp.message_handler()
async def handle_message(message: types.Message):
    print("Пользователь:", message.text)
    try:
        response = openai.ChatCompletion.create(
            model="mistralai/Mistral-7B-Instruct-v0.2",
            messages=[{"role": "user", "content": message.text}]
        )
        reply_text = response['choices'][0]['message']['content']
        print("Ответ GPT:", reply_text)
        await message.reply(reply_text)
    except Exception as e:
        print("Ошибка:", e)
        await message.reply("⚠️ Ошибка при обработке запроса.")
        print("Ошибка:", e)

if __name__ == '__main__':
    print("🤖 Бот запущен и ждет сообщений...")
    executor.start_polling(dp)
