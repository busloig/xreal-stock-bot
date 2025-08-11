import asyncio
import os
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- КНОПКА ---
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Проверить наличие")]
    ],
    resize_keyboard=True
)

# --- ПРОВЕРКА ---
async def check_availability():
    results = []
    async with aiohttp.ClientSession() as session:
        # EU магазин XREAL
        async with session.get("https://eu.shop.xreal.com/products/xreal-air-2-pro") as r:
            text = await r.text()
            results.append("✅ XREAL EU: В наличии" if "Add to cart" in text else "❌ XREAL EU: Нет в наличии")

        # Amazon NL
        async with session.get("https://www.amazon.nl/dp/B0XXXXX") as r:  # замените на реальную ссылку
            text = await r.text()
            results.append("✅ Amazon NL: В наличии" if "Add to Cart" in text else "❌ Amazon NL: Нет в наличии")

        # Unbound XR
        async with session.get("https://unboundxr.nl/xreal-one-pro-l") as r:  # замените на реальную ссылку
            text = await r.text()
            results.append("✅ Unbound XR: В наличии" if "In stock" in text else "❌ Unbound XR: Нет в наличии")

    return "\n".join(results)

# --- ХЕНДЛЕРЫ ---
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Привет! Нажми кнопку, чтобы проверить наличие Xreal One Pro L.", reply_markup=keyboard)

@dp.message(lambda m: m.text == "Проверить наличие")
async def manual_check(message: types.Message):
    await message.answer("🔍 Проверяю наличие...")
    result = await check_availability()
    await message.answer(result)

# --- ЗАПУСК ---
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
