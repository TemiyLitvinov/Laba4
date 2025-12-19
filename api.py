import requests
from config import RAWG_API_KEY


BASE_URL = "https://api.rawg.io/api"


def search_game(name : str):
    url = f"{BASE_URL}/games"
    params = {
        "search": name,
        "key": RAWG_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    if not data["results"]:
        return None

    game_id = data["results"][0]["id"]

    details_url = f"{BASE_URL}/games/{game_id}"
    details_params = {"key": RAWG_API_KEY}
    details_response = requests.get(details_url, params=details_params)

    return details_response.json()


def get_top_games():
    url = f"{BASE_URL}/games"
    params = {
        "ordering" : "-rating",
        "page_size" : 10,
        "key" : RAWG_API_KEY
    }
    response = requests.get(url, params=params)
    return response.json()["results"]