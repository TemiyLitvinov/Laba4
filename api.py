import requests
from config import RAWG_API_KEY


BASE_URL = "https://api.rawg.io/api"


def search_game(name):
    url = f"{BASE_URL}/games"
    params = {
        "search" : name,
        "key" : RAWG_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data["results"][0] if data else None

def get_top_names():
    url = f"{BASE_URL}/games"
    params = {
        "ordering" : "-rating",
        "page_size" : 5,
        "key" : RAWG_API_KEY
    }
    response = requests.get(url, params=params)
    return response.json()["results"]