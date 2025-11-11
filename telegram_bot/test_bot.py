#!/usr/bin/env python3
"""
Тестовий скрипт для перевірки бота
"""

import requests

BOT_TOKEN = "8491626430:AAFcomI07hJc-sEWKPMgc9G2qf38ZurV73E"
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def test_bot():
    """Перевіряє чи бот працює"""
    try:
        response = requests.get(f"{BASE_URL}/getMe")
        data = response.json()
        
        if data.get('ok'):
            bot_info = data.get('result', {})
            print(f"✅ Бот працює!")
            print(f"   Ім'я: {bot_info.get('first_name')}")
            print(f"   Username: @{bot_info.get('username')}")
            print(f"   ID: {bot_info.get('id')}")
            return True
        else:
            print(f"❌ Помилка: {data}")
            return False
    except Exception as e:
        print(f"❌ Помилка підключення: {e}")
        return False

def get_updates():
    """Отримує останні повідомлення"""
    try:
        response = requests.get(f"{BASE_URL}/getUpdates?limit=5")
        data = response.json()
        
        if data.get('ok'):
            updates = data.get('result', [])
            print(f"\n📨 Останні {len(updates)} повідомлень:")
            
            for update in updates:
                if 'message' in update:
                    msg = update['message']
                    text = msg.get('text', '')
                    user = msg.get('from', {})
                    print(f"   • {user.get('first_name')}: {text}")
            
            return True
        else:
            print(f"❌ Помилка: {data}")
            return False
    except Exception as e:
        print(f"❌ Помилка: {e}")
        return False

if __name__ == '__main__':
    print("🤖 Тестування Telegram бота...\n")
    
    if test_bot():
        get_updates()
        print("\n✅ Бот готовий до роботи!")
        print("   Запустіть: python3 bot.py")
    else:
        print("\n❌ Бот не працює. Перевірте токен.")
