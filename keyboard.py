from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/start"), KeyboardButton(text="/help")],
            [KeyboardButton(text="/game"), KeyboardButton(text="/requirements")],
            [KeyboardButton(text="/top")]
        ],
        resize_keyboard=True
    )