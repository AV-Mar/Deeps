from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI
from dummyfile import DummyFile
from config import OPENROUTER_API_KEY, TELEGRAM_TOKEN
import logging

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# OpenRouter клиент с DeepSeek V3 Chat
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    chat_id = update.effective_chat.id
    logging.info(f"Пользователь написал: {user_input}")

    memory = DummyFile()
    memory.write(user_input.encode("utf-8"))
    memory.seek(0)
    prompt = memory.read().decode("utf-8")

    try:
        completion = client.chat.completions.create(
            model="deepseek/deepseek-chat:free",  # теперь DeepSeek V3
            messages=[
                {"role": "system", "content": "Ты умный и дружелюбный ассистент, говорящий на русском языке. Отвечай понятно, логично и по делу."},
                {"role": "user", "content": prompt}
            ]
        )
        response = completion.choices[0].message.content
        logging.info(f"Ответ от DeepSeek V3: {response}")
    except Exception as e:
        response = f"Ошибка: {e}"
        logging.error(f"Ошибка при вызове модели: {e}")

    await context.bot.send_message(chat_id=chat_id, text=response)

# Обработка команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я виртуальный ассистент. Задавай вопросы — помогу чем смогу 🤖")

# Запуск Telegram-бота
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 DeepSeek V3 бот запущен и готов к диалогу!")
    app.run_polling()  # ← вот это обязательно!