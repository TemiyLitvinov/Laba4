import asyncio
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from config import BOT_TOKEN
from api import search_game, get_top_games
from states import GameSearch

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Game_directory_bot\n\n"
        "/game <название> — информация об игре\n"
        "/top — топ 10 игр"
    )

@dp.message(Command("game"))
async def game_command(message: types.Message, state: FSMContext):
    await message.answer("Введите название игры:")
    await state.set_state(GameSearch.waiting_for_name)


@dp.message(GameSearch.waiting_for_name)
async def process_game_name(message: types.Message, state: FSMContext):
    name = message.text
    game = search_game(name)

    if not game:
        await message.answer("Игра не найдена :(")
        await state.clear()
        return

    text = (
        f"🎮 {game['name']}\n"
        f"⭐ Рейтинг: {game['rating']}\n"
        f"📅 Дата выхода: {game['released']}\n\n"
        f"{game['description_raw'][:700]}..."
    )

    image = game.get("background_image")

    if image:
        await message.answer_photo(image, caption=text)
    else:
        await message.answer(text)

    await state.clear()

@dp.message(Command("top"))
async def top_games(message: types.Message):
    games = get_top_games()
    text = "Топ 10 игр:\n\n"

    for i, game in enumerate(games, 1):
        text += f"{i}. {game['name']} — {game['rating']}\n"

    await message.answer(text)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
