import requests
from django.db import IntegrityError

from characters.models import Character
from rick_and_morty_api import settings


def scrape_characters() -> list[Character]:
    url_to_scrape = settings.RICK_AND_MORTY_API_CHARACTERS

    characters = []
    while url_to_scrape is not None:
        characters_response = requests.get(url_to_scrape).json()

        for character_dict in characters_response["results"]:
            characters.append(
                Character(
                    api_id=character_dict["id"],
                    name=character_dict["name"],
                    status=character_dict["status"],
                    species=character_dict["species"],
                    gender=character_dict["gender"],
                    image=character_dict["image"],
                )
            )
        url_to_scrape = characters_response["info"]["next"]
    return characters


def save_characters(characters: list[Character]) -> None:
    for character in characters:
        try:
            character.save()
        except IntegrityError:
            print(f"Character with 'api_id': {character.api_id} already exists in db")


def sync_characters_with_api() -> None:
    characters = scrape_characters()
    save_characters(characters)
