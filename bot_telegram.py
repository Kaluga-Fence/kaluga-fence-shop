# bot_telegram.py
import sqlite3
import time
import requests
import os
from datetime import datetime

# ============= НАСТРОЙКИ =============
BOT_TOKEN = "ВАШ_ТОКЕН"  # ← Замени! Получи у @BotFather
CHAT_ID = "ВАШ_CHAT_ID"  # ← Замени! Узнай через @userinfobot или /getUpdates
DB_PATH = "db.sqlite3"   # Путь к базе Django (если на Render — может быть другим)
CHECK_INTERVAL = 10      # Проверять каждые 10 секунд
# ====================================

def send_telegram_message(text):
    """Отправляет сообщение в Telegram"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Уведомление отправлено")
        else:
            print(f"[Ошибка] Telegram API: {response.status_code}")
    except Exception as e:
        print(f"[Ошибка сети] {e}")

def get_new_orders(last_id):
    """Возвращает новые заказы из базы"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Чтобы можно было обращаться по имени колонки
        cur = conn.cursor()

        cur.execute("SELECT id, name, phone, address, comment, created_at FROM shop_order WHERE id > ? ORDER BY id", (last_id,))
        rows = cur.fetchall()
        conn.close()

        return rows
    except Exception as e:
        print(f"[Ошибка БД] Не могу прочитать db.sqlite3: {e}")
        return []

def format_order_message(order):
    """Форматирует сообщение о заказе"""
    created = datetime.strptime(order['created_at'], "%Y-%m-%d %H:%M:%S.%f%z") if '.' in order['created_at'] else order['created_at']
    return (
        f"📦 <b>НОВЫЙ ЗАКАЗ #{order['id']}</b>\n"
        f"👤 <b>Имя:</b> {order['name']}\n"
        f"📞 <b>Телефон:</b> {order['phone']}\n"
        f"📬 <b>Адрес:</b> {order['address']}\n"
        f"💬 <b>Комментарий:</b> {order['comment'] or 'нет'}\n"
        f"⏰ <b>Время:</b> {created.strftime('%H:%M %d.%m.%Y')}"
    )

def main():
    print("🚀 Telegram-бот запущен. Ожидание новых заказов...")

    # Получаем последний ID при старте
    last_order_id = 0
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT IFNULL(MAX(id), 0) FROM shop_order")
        last_order_id = cur.fetchone()[0]
        conn.close()
        print(f"✅ Последний заказ ID: {last_order_id}. Начинаю слушать...")
    except Exception as e:
        print(f"[Ошибка] Не удалось подключиться к базе: {e}")
        return

    # Основной цикл
    while True:
        new_orders = get_new_orders(last_order_id)
        for order in new_orders:
            message = format_order_message(order)
            send_telegram_message(message)
            last_order_id = order['id']  # Обновляем ID
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
