from typing import List, Any

from CONCORDIA.METIER.BOARD.city import City
from CONCORDIA.METIER.CARDS.architect import Architect
from CONCORDIA.METIER.CARDS.concordia import Concordia
from CONCORDIA.METIER.CARDS.consul import Consul
from CONCORDIA.METIER.CARDS.diplomat import Diplomat
from CONCORDIA.METIER.CARDS.mercator import Mercator
from CONCORDIA.METIER.CARDS.praefectus_magnus import Praefectus_Magnus
from CONCORDIA.METIER.CARDS.prefect import Prefect
from CONCORDIA.METIER.CARDS.senator import Senator
from CONCORDIA.METIER.CARDS.specialist import Specialist
from CONCORDIA.METIER.CARDS.tribune import Tribune
from CONCORDIA.METIER.LINES.way import Way
from CONCORDIA.METIER.god import God
from CONCORDIA.METIER.good import Good
from CONCORDIA.METIER.numeral import Numeral
from CONCORDIA.METIER.CARDS.colonist import Colonist
from CONCORDIA.METIER.player import Player


def find_way_by_name(ways: List[Way], name: str) -> Way:
    """
    Finds a way in a list of ways by its name.

    Args:
        ways (List[Way]): A list of Way objects to search through.
        name (str): The name of the way to find.

    Returns:
        Way: The Way object with the matching name, or None if not found.
    """
    for way in ways:
        if way.way_name == name:
            return way
    return None


def find_city_by_name(cities: List[City], name: str) -> City:
    """
    Finds a city object in a list of cities by its name.

    Args:
        cities (List[City]): A list of City objects to search through.
        name (str): The name of the city to find.

    Returns:
        City: The City object with the matching name, or None if no match is found.
    """
    for city in cities:
        if city.city_name == name:
            return city
    return None


def find_token_by_rom_char(tokens: dict, rom_char: str) -> Any | None:
    """
    Finds a token in a dictionary of tokens based on its roman character representation.

    Args:
        tokens (dict): A dictionary of tokens.
        rom_char (str): The roman character representation of the token to be found.

    Returns:
        dict: The token with the matching roman character representation, or None if not found.
    """
    for token in tokens:
        if (token['CITY_TOKEN_ROMAN_CHAR'] == rom_char
                and token['CITY_TOKEN_N_COPIES'] > 0):
            return token
    return None


def find_god_by_name(gods: List[God], name: str) -> God | None:
    """
    Finds a God object in a list of Gods by name.

    Args:
        gods (List[God]): A list of God objects to search through.
        name (str): The name of the God to find.

    Returns:
        God: The God object with the specified name, or None if no such God exists.
    """
    for god in gods:
        if god.god_name == name:
            return god
    return None


def find_good_by_name(goods: List[Good], name: str) -> Good | None:
    """
    Finds a Good object in a list of Good objects by its name.

    Args:
        goods (List[Good]): A list of Good objects to search through.
        name (str): The name of the Good object to find.

    Returns:
        Good: The Good object with the specified name, or None if it is not found.
    """
    for good in goods:
        if good.good_name == name:
            return good
    return None


def find_numeral_by_roman(numerals: List[Numeral], roman: str) -> Numeral | None:
    """
    Finds a Numeral object in a list of Numeral objects by its Roman numeral representation.

    Args:
        numerals (List[Numeral]): A list of Numeral objects to search through.
        roman (str): The Roman numeral representation of the Numeral object to find.

    Returns:
        Numeral: The Numeral object with the matching Roman numeral representation, or None if not found.
    """
    for numeral in numerals:
        if numeral.numeral_roman == roman:
            return numeral
    return None


def find_card_type_by_card_name(card_name: str):
    """
    Given a card name, returns the corresponding card type.

    Args:
    - card_name (str): the name of the card to find the type for.

    Returns:
    - type: the type of the card corresponding to the given name.
    """
    card_name = card_name.lower()
    match card_name:
        case "colonist":
            return Colonist
        case "concordia":
            return Concordia
        case "consul":
            return Consul
        case "diplomat":
            return Diplomat
        case "senator":
            return Senator
        case "tribune":
            return Tribune
        case "mercator":
            return Mercator
        case "architect":
            return Architect
        case "præfectvs magnvs":
            return Praefectus_Magnus
        case "prefect":
            return Prefect
        case "mason" | "farmer" | "smith" | "vintner" | "weaver":
            return Specialist


def find_house_by_player(houses: List, player: Player):
    player_houses = []
    for house in houses:
        if house.house_player == player:
            player_houses.append(house)
    return player_houses


print()
