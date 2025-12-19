import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import BOT_TOKEN
from api import search_game, get_top_games

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Game_directory_bot\n\n"
        "/game <название> — информация об игре\n"
        "/top — топ 10 игр"
    )


@dp.message(Command("game"))
async def game_info(message: types.Message):
    parts = message.text.split(maxsplit=1)

    if len(parts) < 2:
        await message.answer("Введите название игры:")
        return

    name = parts[1]
    game = search_game(name)

    if game:
        text = (
            f"🎮 {game['name']}\n"
            f"⭐ Рейтинг: {game['rating']}\n"
            f"📅 Дата выхода: {game['released']}"
        )
    else:
        text = "Игра не найдена :("

    await message.answer(text)


@dp.message(Command("top"))
async def top_games(message: types.Message):
    games = get_top_games()
    text = "🏆 Топ 10 игр:\n\n"

    for i, game in enumerate(games, 1):
        text += f"{i}. {game['name']} — {game['rating']}\n"

    await message.answer(text)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
