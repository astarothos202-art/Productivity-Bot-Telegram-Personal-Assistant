import os

# Токен бота (вставьте свой токен прямо сюда)
BOT_TOKEN = "BOT_TOKEN"

if not BOT_TOKEN or BOT_TOKEN == "ВАШ_ТОКЕН_СЮДА":
    raise ValueError("❌ Токен не найден! Вставьте свой токен в config.py")