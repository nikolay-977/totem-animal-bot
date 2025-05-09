import os
import logging
from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
from handlers import start, help_command, quiz, button, collect_feedback

# Загружаем переменные окружения
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    # Создаем экземпляр приложения
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("quiz", quiz))
    application.add_handler(CallbackQueryHandler(button))     # Обработчик нажатий кнопок
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, collect_feedback))  # Обработчик текстовых сообщений для отзывов

    # Запускаем бота
    application.run_polling()

if __name__ == "__main__":
    main()
