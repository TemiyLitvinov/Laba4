from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/game"), KeyboardButton(text="/requirements")],
            [KeyboardButton(text="/top"), KeyboardButton(text="/help")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
