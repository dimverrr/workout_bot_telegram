import requests
import random
from config_reader import config


def request_exercice(body_part: str, number_of_exercices: str):
    url = f"https://exercisedb.p.rapidapi.com/exercises/bodyPart/{body_part}"

    headers = {
        "X-RapidAPI-Key": config.api_key.get_secret_value(),
        "X-RapidAPI-Host": "exercisedb.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers)
    exercices = random.choices(response.json(), k=int(number_of_exercices))
    return exercices
