import urllib.parse
import os
import logging
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from data import questions, results
from telegram import Bot

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
STAFF_CHAT_ID = os.getenv("STAFF_CHAT_ID")

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"User {user.id} started the bot with /start")
    welcome_text = (
        "Привет! 🐾 Добро пожаловать в викторину «Какое у тебя тотемное животное?»\n\n"
        "Я помогу тебе узнать, какое животное из Московского зоопарка — твой тотем.\n"
        "Для начала используй команду /quiz и просто выбирай варианты ответа на вопросы.\n\n"
        "В любой момент ты можешь написать /start чтобы вернуться сюда.\n"
        "Если нужна помощь, пиши /help."
    )
    await update.message.reply_text(welcome_text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Как пройти викторину:\n"
        "- Нажми /quiz, чтобы начать.\n"
        "- Выбирай один из вариантов на каждый вопрос нажатием кнопок.\n"
        "- В конце ты увидишь своё тотемное животное с описанием и картинкой.\n"
        "- После результата доступны кнопки:\n"
        "  📋 Узнать больше — информация о программе опеки.\n"
        "  🔁 Попробовать ещё раз — пройти викторину заново.\n"
        "  💬 Оставить отзыв — поделиться впечатлениями.\n"
        "  📞 Связаться с сотрудником — задать вопросы сотрудникам зоопарка.\n\n"
        "Если что-то пошло не так, это сообщение поможет!"
    )
    await update.message.reply_text(help_text)

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"User {user.id} started the quiz with /quiz")
    context.user_data['answers'] = []
    await send_next_question(update, context)


async def send_next_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    index = len(context.user_data['answers'])
    if index >= len(questions):
        await show_result(update, context)
        return

    q = questions[index]
    keyboard = [
        [InlineKeyboardButton(opt["text"], callback_data=str(i))] for i, opt in enumerate(q["options"])
    ]
    markup = InlineKeyboardMarkup(keyboard)

    try:
        if update.callback_query:
            await update.callback_query.message.reply_text(q["question"], reply_markup=markup)
        else:
            await update.effective_chat.send_message(q["question"], reply_markup=markup)
    except Exception as e:
        logger.exception(f"Failed to send question {index + 1}: {e}")


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = update.effective_user
    await query.answer()

    data = query.data
    logger.info(f"User {user.id} clicked button: {data}")

    if data == "restart":
        context.user_data['answers'] = []
        await query.message.reply_text("Давайте начнём заново!")
        await send_next_question(update, context)

    elif data == "info":
        await query.message.reply_text(
            "🐾 Узнай больше о программе опеки: https://moscowzoo.ru/my-zoo/become-a-guardian/"
        )

    elif data == "contact":
        await send_result_to_staff(update, context)

    elif data == "feedback":
        await query.message.reply_text("Пожалуйста, напишите свой отзыв. Мы обязательно учтем ваше мнение.")
        context.user_data['feedback'] = True

    else:
        try:
            context.user_data.setdefault('answers', []).append(int(data))
            await send_next_question(update, context)
        except ValueError:
            logger.warning(f"Unexpected callback data: {data}")
            await query.message.reply_text("Произошла ошибка. Попробуйте ещё раз.")


async def show_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answers = context.user_data.get('answers', [])
    score = sum(answers) % len(results)
    name, image_path, description = results[score]

    bot_username = (await context.bot.get_me()).username
    share_link = f"https://t.me/{bot_username}"
    share_text = f"🎉 Мой тотем — {name}! Пройди тест в боте 👉 @{bot_username}"

    encoded_share_text = urllib.parse.quote(share_text)
    encoded_share_link = urllib.parse.quote(share_link)

    buttons = [
        [InlineKeyboardButton("📋 Узнать больше", callback_data="info")],
        [InlineKeyboardButton("🔁 Попробовать ещё раз", callback_data="restart")],
        [InlineKeyboardButton("📤 Поделиться в Telegram",
                              url=f"https://t.me/share/url?url={encoded_share_link}&text={encoded_share_text}"),
         InlineKeyboardButton("📤 Поделиться в VK",
                              url=f"https://vk.com/share.php?url={encoded_share_link}&title={encoded_share_text}")],
        [InlineKeyboardButton("📞 Связаться с сотрудником", callback_data="contact")],
        [InlineKeyboardButton("💬 Оставить отзыв", callback_data="feedback")]
    ]

    try:
        with open(image_path, 'rb') as photo:
            await update.effective_chat.send_photo(
                photo=photo,
                caption=f"🎉 Ты — {name}!\n\n{description}\n\nХочешь узнать больше о программе опеки или пройти заново?",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        logger.info(f"User {update.effective_user.id} got result: {name}")
    except Exception as e:
        logger.exception(f"Failed to send result for user {update.effective_user.id}: {e}")
        await update.effective_chat.send_message("Произошла ошибка при отправке результата.")


async def send_result_to_staff(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Получаем результат теста
    answers = context.user_data.get('answers', [])
    score = sum(answers) % len(results)
    name, image_path, description = results[score]
    user_username = update.effective_user.username
    if user_username:
        user_info = f"{update.effective_user.full_name} (@{update.effective_user.username})"
    else:
        user_info = f"{update.effective_user.full_name}"

    # Формируем сообщение для сотрудника
    message = f"Пользователь прошел тест! Вот его результат:\n\n" \
              f"Тотемное животное: {name}\n" \
              f"Описание: {description}\n\n" \
              f"Результаты викторины:\n{', '.join(str(ans) for ans in answers)}\n\n" \
              f"Пользователь: {user_info}\n" \
              f"Чат ID: https://web.telegram.org/a/#{update.effective_chat.id}"

    # Отправляем сообщение сотруднику через Telegram
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        await bot.send_message(chat_id=STAFF_CHAT_ID, text=message)
        await update.callback_query.message.reply_text(
            "Ваш запрос отправлен сотруднику зоопарка! Скоро с вами свяжутся.")
    except Exception as e:
        logger.exception(f"Failed to send message to staff: {e}")
        await update.callback_query.message.reply_text("Произошла ошибка при отправке запроса.")

async def handle_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # Сбор отзыва
    feedback = update.message.text
    logger.info(f"Received feedback from {user.id}: {feedback}")

    # Отправляем отзыв сотруднику
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        user_username = update.effective_user.username
        if user_username:
            user_info = f"{update.effective_user.full_name} (@{update.effective_user.username})"
        else:
            user_info = f"{update.effective_user.full_name} (https://web.telegram.org/a/#{update.effective_chat.id})"
        feedback_message = (
            f"Новый отзыв от пользователя {user_info}:\n\n{feedback}"
        )
        await bot.send_message(chat_id=STAFF_CHAT_ID, text=feedback_message)
        await update.message.reply_text("Спасибо за ваш отзыв! Мы обязательно учтем его.")
    except Exception as e:
        logger.exception(f"Failed to send feedback to staff: {e}")
        await update.message.reply_text("Произошла ошибка при отправке отзыва.")
async def collect_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Проверяем, что у пользователя есть флаг обратной связи
    if context.user_data.get('feedback'):
        # Переводим пользователя в режим сбора отзыва
        await handle_feedback(update, context)
        context.user_data['feedback'] = False
