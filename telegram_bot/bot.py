#!/usr/bin/env python3
"""
TimeKeeper Telegram Backup Bot
Простий бот для авторизації та зберігання бекапів
"""

import os
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
BOT_TOKEN = "8491626430:AAFcomI07hJc-sEWKPMgc9G2qf38ZurV73E"

# Словник для зберігання кодів авторизації (в пам'яті)
auth_codes = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробник команди /start - генерує код авторизації"""
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    # Очищаємо старі коди (старше 5 хвилин)
    current_time = time.time()
    expired_codes = [k for k, v in auth_codes.items() 
                     if current_time - v.get('timestamp', 0) > 300]
    for code in expired_codes:
        del auth_codes[code]
    
    # Генеруємо 6-значний код
    code = str(random.randint(100000, 999999))
    
    # Зберігаємо код з інформацією про користувача
    auth_codes[code] = {
        'chat_id': chat_id,
        'user_name': f"{user.first_name} {user.last_name or ''}".strip(),
        'username': user.username,
        'timestamp': time.time()
    }
    
    welcome_message = f"""
🔐 <b>TimeKeeper</b>

Ваш код: <code>{code}</code>

📱 Введіть цей код в додатку

⏱ Дійсний 5 хвилин
"""
    
    await update.message.reply_text(
        welcome_message,
        parse_mode='HTML'
    )
    
    logger.info(f"✅ Code {code} for {user.first_name} (chat_id: {chat_id})")
    logger.info(f"📊 Active codes: {len(auth_codes)}")


async def verify_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда для перевірки коду (викликається з додатку)"""
    # Ця команда не буде викликатись користувачем
    # Вона для внутрішнього використання
    pass


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробник текстових повідомлень"""
    text = update.message.text.strip()
    
    # Перевіряємо чи це код для верифікації (формат: verify:123456)
    if text.startswith("verify:"):
        code = text.replace("verify:", "")
        if code in auth_codes:
            user_data = auth_codes[code]
            response = f"✅ Code valid: {user_data['chat_id']}|{user_data['user_name']}"
            await update.message.reply_text(response)
            logger.info(f"✅ Code {code} verified")
        else:
            await update.message.reply_text("❌ Code not found")
            logger.warning(f"❌ Code {code} not found")
        return
    
    help_message = """
ℹ️ <b>Як підключитись:</b>

1. Натисніть /start щоб отримати код
2. Введіть код в додатку TimeKeeper
3. Готово!

📦 Всі ваші бекапи будуть зберігатись тут.
"""
    
    await update.message.reply_text(help_message, parse_mode='HTML')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробник команди /help"""
    help_text = """
📖 <b>Довідка TimeKeeper Backup Bot</b>

<b>Команди:</b>
/start - Почати роботу з ботом
/help - Показати цю довідку
/status - Перевірити статус підключення

<b>Як користуватись:</b>
1. Підключіть бота в додатку TimeKeeper
2. Бот автоматично зберігатиме ваші бекапи
3. Всі файли будуть у цьому чаті
4. Ви зможете завантажити їх в будь-який момент

<b>Безпека:</b>
• Дані зберігаються тільки у вашому чаті
• Ніхто інший не має доступу
• Файли зашифровані Telegram

Якщо у вас виникли питання, зверніться до розробника: @deonisiyon
"""
    
    await update.message.reply_text(
        help_text,
        parse_mode='HTML'
    )


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробник команди /status"""
    chat_id = update.effective_chat.id
    
    # Тут можна додати перевірку чи користувач авторизований
    # Поки що просто показуємо базову інформацію
    
    status_text = f"""
📊 <b>Статус підключення</b>

Chat ID: <code>{chat_id}</code>

Якщо ви підключили бота в додатку, всі бекапи будуть автоматично надсилатись в цей чат.

Для повторного підключення використайте команду /start
"""
    
    await update.message.reply_text(
        status_text,
        parse_mode='HTML'
    )


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
    logger.info("Bot started!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
