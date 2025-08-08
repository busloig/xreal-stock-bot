import asyncio
import os
import requests
from aiogram import Bot
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", 360))
URL_XREAL = os.getenv("URL_XREAL")
URL_AMAZON = os.getenv("URL_AMAZON")
URL_UNBOUND = os.getenv("URL_UNBOUND")

bot = Bot(token=BOT_TOKEN)

def check_site(url, sold_out_markers):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        text = resp.text.lower()
        for marker in sold_out_markers:
            if marker.lower() in text:
                return None
        return True
    except Exception as e:
        return None

async def main():
        await bot.send_message(CHAT_ID, "✅ Тест: бот запущен и работает!")
    while True:
        messages = []

        if check_site(URL_XREAL, ["sold out", "out of stock"]):
            messages.append(f"🎉 One Pro L доступна в EU-магазине!\n{URL_XREAL}")
        if check_site(URL_AMAZON, ["currently unavailable", "derzeit nicht verfügbar"]):
            messages.append(f"📦 One Pro L доступна на Amazon NL!\n{URL_AMAZON}")
        if check_site(URL_UNBOUND, ["sold out", "out of stock"]):
            messages.append(f"🏢 One Pro L доступна у Unbound XR!\n{URL_UNBOUND}")

        for msg in messages:
            await bot.send_message(CHAT_ID, msg)

        await asyncio.sleep(CHECK_INTERVAL_MINUTES * 60)

if __name__ == "__main__":
    asyncio.run(main())
