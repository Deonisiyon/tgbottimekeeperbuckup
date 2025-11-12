#!/usr/bin/env python3
"""
TimeKeeper Telegram Backup Bot
Простий бот для авторизації та зберігання бекапів
"""

import logging
import random
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен бота
BOT_TOKEN = "8491626430:AAF9uFuvaAlRDTu_kWXvYsIYS94JcHygCnQ"

# Словник для зберігання кодів авторизації (в пам'яті)
auth_codes = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробник команди /start - показує chat_id"""
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    welcome_message = f"""
🔐 <b>TimeKeeper Backup</b>

Привіт, {user.first_name}!

Ваш Chat ID: <code>{chat_id}</code>

📱 <b>Як підключитись:</b>
1. Скопіюйте Chat ID вище
2. Відкрийте додаток TimeKeeper
3. Вставте Chat ID в поле
4. Натисніть "Підключити"

✅ Після підключення всі бекапи будуть автоматично надсилатись сюди!
"""
    
    # Відправляємо повідомлення користувачу
    await update.message.reply_text(
        welcome_message,
        parse_mode='HTML'
    )
    
    logger.info(f"✅ User {user.first_name} (chat_id: {chat_id}) opened bot")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробник команди /help"""
    help_text = """
ℹ️ <b>Як підключитись:</b>

1. Натисніть /start щоб отримати код
2. Введіть код в додатку TimeKeeper
3. Готово!

📦 Всі ваші бекапи будуть зберігатись тут.

💬 Розробник: @deonisiyon
"""
    
    await update.message.reply_text(
        help_text,
        parse_mode='HTML'
    )


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробник команди /status"""
    chat_id = update.effective_chat.id
    
    status_text = f"""
📊 <b>Статус</b>

Chat ID: <code>{chat_id}</code>

Якщо ви підключили бота в додатку, всі бекапи будуть автоматично надсилатись в цей чат.

Для повторного підключення використайте /start
"""
    
    await update.message.reply_text(
        status_text,
        parse_mode='HTML'
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробник текстових повідомлень"""
    help_message = """
ℹ️ <b>Як підключитись:</b>

1. Натисніть /start щоб отримати код
2. Введіть код в додатку TimeKeeper
3. Готово!

📦 Всі ваші бекапи будуть зберігатись тут.
"""
    
    await update.message.reply_text(help_message, parse_mode='HTML')


def main() -> None:
    """Запуск бота"""
    # Створюємо додаток
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Додаємо обробники
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запускаємо бота
    logger.info("🤖 Bot started!")
    logger.info("📱 Username: @backuptimekeeper_bot")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
