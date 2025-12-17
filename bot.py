import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import BOT_TOKEN


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: types.Message):
    text = (
        "Game_directory_bot\n"
        "/game <название> - получить информацию об игре"
    )
    await message.answer(text)