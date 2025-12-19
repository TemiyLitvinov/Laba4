class BotError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class InvalidGameNameError(BotError):
    def __init__(self, message='Некорректное название игры'):
        super().__init__(message)


class GameNotFoundError(BotError):
    def __init__(self, message='Игра не найдена'):
        super().__init__(message)


class ApiRequestError(BotError):
    def __init__(self, message='Ошибка при запросе к API'):
        super().__init__(message)