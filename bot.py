import asyncio
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from googletrans import Translator
from states import RequirementsSearch
from keyboard import main_keyboard


from config import BOT_TOKEN
from api import search_game, get_top_games
from states import GameSearch

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
translator = Translator()


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "🎮 Game_directory_bot\n"
        "Бот для получения информации о компьютерных играх.\n\n"
        "Используйте кнопки ниже ⬇️",
        reply_markup=main_keyboard()
    )


@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer(
        "📖 Доступные команды:\n\n"
        "/game — поиск информации об игре\n"
        "/top — топ 10 игр\n"
        "/requirements - просмотр системных требований к игре\n"
    )


@dp.message(Command("game"))
async def game_command(message: types.Message, state: FSMContext):
    await message.answer("Введите название игры:")
    await state.set_state(GameSearch.waiting_for_name)


@dp.message(GameSearch.waiting_for_name)
async def process_game_name(message: types.Message, state: FSMContext):
    name = message.text
    game = search_game(name)
    description = game['description_raw']
    translated_description = translator.translate(description, dest="ru").text

    if not game:
        await message.answer("Игра не найдена :(")
        await state.clear()
        return


    text = (
        f"🎮 {game['name']}\n"
        f"⭐ Рейтинг: {game['rating']}\n"
        f"📅 Дата выхода: {game['released']}\n\n"
        f"{translated_description[:700]}..."
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


@dp.message(Command("requirements"))
async def requirements_command(message: types.Message, state: FSMContext):
    await message.answer("Введите название игры для просмотра системных требований 💻")
    await state.set_state(RequirementsSearch.waiting_for_name)


@dp.message(RequirementsSearch.waiting_for_name)
async def process_requirements(message: types.Message, state: FSMContext):
    name = message.text
    game = search_game(name)

    if not game:
        await message.answer("Игра не найдена :(")
        await state.clear()
        return

    requirements_text = "💻 Системные требования:\n\n"
    found = False

    for platform in game.get("platforms", []):
        if platform["platform"]["name"] == "PC":
            reqs = platform.get("requirements", {})
            requirements_text += (
                f"{reqs.get('minimum', 'Нет данных минимальных требований')}\n\n"
                f"{reqs.get('recommended', 'Нет данных рекомендуемых требований')}"
            )
            found = True
            break

    if not found:
        requirements_text = "Системные требования не найдены :("

    translated_requirements = translator.translate(requirements_text, dest="ru").text

    await message.answer(translated_requirements)
    await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())