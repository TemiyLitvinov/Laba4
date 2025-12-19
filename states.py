from aiogram.fsm.state import State, StatesGroup


class GameSearch(StatesGroup):
    waiting_for_name = State()


class RequirementsSearch(StatesGroup):
    waiting_for_name = State()