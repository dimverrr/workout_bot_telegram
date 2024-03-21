import requests
from config_reader import config
import numpy as np


def request_exercice(body_part: str, number_of_exercices: str):
    url = f"https://exercisedb.p.rapidapi.com/exercises/bodyPart/{body_part}"
    querystring = {"limit": "203"}

    headers = {
        "X-RapidAPI-Key": config.api_key.get_secret_value(),
        "X-RapidAPI-Host": "exercisedb.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers, params=querystring)
    exercices = np.random.choice(
        response.json(), int(number_of_exercices), replace=False
    )
    return exercices
