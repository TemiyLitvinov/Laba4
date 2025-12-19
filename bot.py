import asyncio
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from googletrans import Translator
from states import RequirementsSearch
from keyboard import main_keyboard
from exceptions import InvalidGameNameError, GameNotFoundError, ApiRequestError
from api import get_game_requirements



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
    try:
        name = message.text.strip()

        if name.isdigit():
            raise InvalidGameNameError("Название игры не может состоять только из чисел")

        if len(name) < 2:
            raise InvalidGameNameError("Название игры слишком короткое")

        game = search_game(name)

        description = game.get("description_raw", "Описание отсутствует")
        translated_description = translator.translate(description, dest="ru").text

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

    except InvalidGameNameError as e:
        await message.answer(f"{e}")

    except GameNotFoundError:
        await message.answer("Игра не найдена. Попробуйте другое название.")

    except ApiRequestError:
        await message.answer("Ошибка сервера. Попробуйте позже.")

    finally:
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
    try:
        name = message.text.strip()

        if name.isdigit():
            raise InvalidGameNameError("Название игры не может быть числом")

        reqs = get_game_requirements(name)

        requirements_text = (
            f"{reqs['minimum']}\n\n"
            f"{reqs['recommended']}"
        )

        translated = translator.translate(requirements_text, dest="ru").text
        await message.answer(translated)

    except InvalidGameNameError as e:
        await message.answer(f"{e}")

    except GameNotFoundError:
        await message.answer("Игра не найдена. Попробуйте другое название.")

    except ApiRequestError:
        await message.answer("Ошибка соединения с сервером RAWG. Попробуйте позже.")

    finally:
        await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())