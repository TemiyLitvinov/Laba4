import requests
from config import RAWG_API_KEY
from exceptions import GameNotFoundError, ApiRequestError

BASE_URL = "https://api.rawg.io/api"


def search_game(name: str):
    try:
        url = f"{BASE_URL}/games"
        params = {
            "search": name,
            "key": RAWG_API_KEY
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        if not data.get("results"):
            raise GameNotFoundError("Игра не найдена")

        game_id = data["results"][0]["id"]

        details_url = f"{BASE_URL}/games/{game_id}"
        details_response = requests.get(details_url, params={"key": RAWG_API_KEY}, timeout=10)
        details_response.raise_for_status()

        return details_response.json()

    except requests.RequestException:
        raise ApiRequestError("Ошибка соединения с сервером RAWG")


def get_top_games():
    try:
        url = f"{BASE_URL}/games"
        params = {
            "ordering": "-rating",
            "page_size": 10,
            "key": RAWG_API_KEY
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        return response.json()["results"]

    except requests.RequestException:
        raise ApiRequestError("Ошибка получения списка игр")

def get_game_requirements(name: str):
    try:
        game = search_game(name)

        for platform in game.get("platforms", []):
            if platform["platform"]["name"].lower() == "pc":
                requirements = platform.get("requirements", {})
                return {
                    "minimum": requirements.get("minimum", "Минимальные требования отсутствуют"),
                    "recommended": requirements.get("recommended", "Рекомендуемые требования отсутствуют")
                }

        return {
            "minimum": "Системные требования для PC отсутствуют",
            "recommended": "Системные требования для PC отсутствуют"
        }

    except GameNotFoundError:
        raise GameNotFoundError("Игра не найдена")

    except requests.RequestException:
        raise ApiRequestError("Ошибка соединения с сервером RAWG")