import random
from typing import List

import CONCORDIA.DAL.database_data as db
from CONCORDIA.HELPER.find_helper import (find_city_by_name, find_way_by_name,
                                          find_token_by_rom_char,
                                          find_god_by_name, find_good_by_name,
                                          find_numeral_by_roman,
                                          find_card_type_by_card_name)
from CONCORDIA.METIER.BOARD.city import City
from CONCORDIA.METIER.BOARD.map import Map
from CONCORDIA.METIER.BOARD.province import Province
from CONCORDIA.METIER.display_area import DisplayArea
from CONCORDIA.METIER.good import Good
from CONCORDIA.METIER.god import God
from CONCORDIA.METIER.LINES.line import Line
from CONCORDIA.METIER.LINES.way import Way
from CONCORDIA.METIER.CARDS.card import Card
from CONCORDIA.METIER.numeral import Numeral
from CONCORDIA.METIER.sdo_point import SDOPoint


def data_to_sdo_point(data: dict) -> SDOPoint:
    """
    Converts a dictionary of X and Y coordinates to an SDOPoint object.

    Args:
        data (dict): A dictionary containing the X and Y coordinates.

    Returns:
        SDOPoint: An SDOPoint object with the X and Y coordinates.
    """
    return SDOPoint(
        data['X'],
        data['Y']
    )


def data_to_city(data: dict, capital=False) -> City:
    """
    Converts data to a City object.

    Args:
        data (dict): A dictionary containing city data.
        capital (bool, optional): Whether the city is a capital or not.
            Defaults to False.

    Returns:
        City: A City object.
    """
    return City(
        data['CITY_NAME'],
        data['CITY_ROMAN_CHAR'],
        capital,
        data_to_sdo_point(data['CITY_COORDINATES']),
        [],
        []
    )


def data_to_province(data: dict, numerals: List[Numeral]) -> Province:
    """
    Converts a dictionary of province data to a Province object.

    Args:
        data (dict): A dictionary containing province data.
        numerals (List[Numeral]): A list of Numeral objects.

    Returns:
        Province: A Province object created from the given data.
    """
    citys = []
    for city in data['PROVINCE_CITY']:
        citys.append(data_to_city(city))
    return Province(
        data['PROVINCE_NAME'],
        find_numeral_by_roman(numerals, data['PROVINCE_ROMAN_NUM']),
        citys,
        data_to_sdo_point(data['PROVINCE_COORDINATES']),
        None
    )


def data_to_way(line_type: dict) -> Way:
    """
    Converts a dictionary of line_type data to a Way object.

    Args:
        line_type (dict): A dictionary containing the data for a line_type.

    Returns:
        Way: A Way object with the data from the line_type dictionary.
    """
    return Way(
        line_type['WAY_NAME'],
        line_type['WAY_COLOR']
    )


def data_to_line(data: dict, citys: List[City], ways: List[Way]) -> Line:
    """
    Converts data to a Line object.

    Args:
        data: A dictionary containing data for a Line object.
        citys: A list of City objects.
        ways: A list of Way objects.

    Returns:
        A Line object.
    """
    return Line(
        find_city_by_name(citys, data['LINE_CITY_1']),
        find_city_by_name(citys, data['LINE_CITY_2']),
        None,
        find_way_by_name(ways, data['LINE_WAY'])
    )


def data_to_map(data: dict, capital: City, provinces: List[Province],
                lines: List[Line]) -> Map:
    """
    Converts a dictionary of map data to a Map object.

    Args:
        data (Dict[str, any]): A dictionary containing map data.
        capital (City): The capital city of the map.
        provinces (List[Province]): A list of provinces in the map.
        lines (List[Line]): A list of lines in the map.

    Returns:
        Map: A Map object representing the map data.
    """
    return Map(
        data['MAP_NAME'],
        data['MAP_MIN_N_PLAYERS'],
        data['MAP_MAX_N_PLAYERS'],
        capital,
        provinces,
        data_to_sdo_point(data['MAP_MAX_COORDINATES']),
        lines
    )


def data_to_god(data: dict) -> God:
    """
    Converts a dictionary of data to a God object.

    Args:
        data (dict): A dictionary containing the data for a God object.

    Returns:
        God: A God object created from the data in the dictionary.
    """
    return God(
        data['GOD_NAME'],
        data['GOD_EXAMPLE'],
        data['GOD_SIGNIFICANCE'],
        data['GOD_REWARD'],
        data['GOD_VICTORY_POINTS']
    )


def data_to_card(data: dict, gods: List[God], goods: List[Good],
                 numerals: List[Numeral]) -> Card:
    """
    Converts a dictionary of data into a Card object.

    Args:
        data (dict): A dictionary containing data for the card.
        gods (List[God]): A list of God objects.
        goods (List[Good]): A list of Good objects.
        numerals (List[Numeral]): A list of Numeral objects.

    Returns:
        Card: A Card object created from the data.
    """
    god = find_god_by_name(gods, data['CARD_GOD'])
    goods_cost = []
    if data['CARD_FOR_SALE_COST'] is not None:
        for good in data['CARD_FOR_SALE_COST']:
            goods_cost.append(find_good_by_name(goods, good))
    for_sale_deck = []
    if data['CARD_FOR_SALE_DECK'] is not None:
        for roman in data['CARD_FOR_SALE_DECK']:
            for_sale_deck.append(find_numeral_by_roman(numerals, roman))
    current_card = find_card_type_by_card_name(data['CARD_NAME'])(
        data['CARD_NAME'],
        data['CARD_ACTION'],
        data['CARD_EXAMPLE'],
        god,
        for_sale_deck,
        goods_cost
    )

    if current_card.card_name == "MASON":
        current_card.speciality = find_good_by_name(goods, "brick")
    elif current_card.card_name == "FARMER":
        current_card.speciality = find_good_by_name(goods, "food")
    elif current_card.card_name == "SMITH":
        current_card.speciality = find_good_by_name(goods, "tool")
    elif current_card.card_name == "VINTNER":
        current_card.speciality = find_good_by_name(goods, "wine")
    elif current_card.card_name == "WEAVER":
        current_card.speciality = find_good_by_name(goods, "cloth")

    return current_card


def data_to_numeral(data: dict) -> Numeral:
    """
    Converts a dictionary of numeral data to a Numeral object.

    Args:
        data (dict): A dictionary containing the numeral data.

    Returns:
        Numeral: A Numeral object with the converted data.
    """
    return Numeral(
        data['NUMERAL_ARABIC'],
        data['NUMERAL_ROMAN']
    )


def data_to_display_area(data: dict, goods: List[Good]) -> DisplayArea:
    """
    Converts a dictionary of display area data into a DisplayArea object.

    Args:
        data (dict): A dictionary containing display area data.
        goods (List[Good]): A list of Good objects.

    Returns:
        DisplayArea: A DisplayArea object created from the input data.
    """
    return DisplayArea(
        data['DISPLAY_AREA_ANY_GOOD_REQUIRED'] == "Y",
        data['DISPLAY_AREA_N_GOODS'],
        data['DISPLAY_AREA_POSITION'],
        find_good_by_name(goods, data['DISPLAY_AREA_GOOD'])
    )


def fill_way() -> List[Way]:
    """
    Retrieves all ways from the database and converts them to Way objects.

    Returns:
        A list of Way objects.
    """
    ways = db.get_concordia_ways()
    ways_list = []
    for line_type in ways:
        ways_list.append(
            data_to_way(line_type)
        )
    return ways_list


def fill_goods() -> List[Good]:
    """
    Retrieves a list of goods from the database and converts them into a list
        of Good objects.

    Returns:
        A list of Good objects.
    """
    goods = db.get_concordia_goods()
    goods_list = []
    for good in goods:
        goods_list.append(
            Good(good['GOOD_NAME'], good['GOOD_VALUE'], good['GOOD_COLOR'])
        )
    return goods_list


def fill_map(map_id: int, ways: List[Way], numerals: List[Numeral]) -> Map:
    """
    Fills a map object with data from the database.

    Args:
        numerals:
        map_id (int): The ID of the map to retrieve from the database.
        ways (List[Way]): A list of Way objects to use when creating Line
            objects.

    Returns:
        Map: A Map object filled with data from the database.
    """
    map_data = db.get_concordia_map()
    provinces = []
    lines = []
    capital = data_to_city(map_data[map_id]['MAP_CAPITAL'], True)

    for province in map_data[map_id]['MAP_PROVINCE']:
        current_province = data_to_province(province, numerals=numerals)
        provinces.append(current_province)

    citys = []
    for province in provinces:
        for city in province.province_coll_citys:
            citys.append(city)
    citys.append(capital)

    for line in map_data[map_id]['MAP_LINE']:
        current_line = data_to_line(line, citys, ways)
        lines.append(current_line)

    return data_to_map(map_data[map_id], capital, provinces, lines)


def fill_city_token(citys: List[City]):
    """
    Assigns a random city token to each city in the given list of cities,
        and updates the city's goods cost
    based on the assigned token. Decrements the number of copies of the
        assigned token by 1.

    Args:
        citys (List[City]): A list of City objects to assign tokens to.

    Returns:
        None
    """
    city_tokens = db.get_concordia_city_tokens()
    random.shuffle(citys)
    for city in citys:
        current_city_token = find_token_by_rom_char(
            city_tokens, city.city_roman_char
        )
        if current_city_token is not None:
            goods = fill_goods()
            for g in goods:
                if g.good_name == current_city_token['CITY_TOKEN_GOOD']:
                    city.city_good = g
                    current_city_token['CITY_TOKEN_N_COPIES'] -= 1


def fill_gods() -> List[God]:
    """
    Retrieves all gods from the database and converts them to a list of God
        objects.

    Returns:
        List[God]: A list of God objects.
    """
    gods = db.get_concordia_gods()
    gods_list = []
    for god in gods:
        gods_list.append(data_to_god(god))
    return gods_list


def fill_numerals() -> List[Numeral]:
    """
    Retrieves all numerals from the database and converts them to Numeral
        objects.

    Returns:
        A list of Numeral objects.
    """
    numerals = db.get_concordia_numerals()
    numerals_list = []
    for numeral in numerals:
        numerals_list.append(data_to_numeral(numeral))
    return numerals_list


def fill_cards(gods: List[God], goods: List[Good],
               numerals: List[Numeral]) -> List[Card]:
    """
    Returns a list of Card objects created from the data retrieved from the
        database.

    Args:
        gods (List[God]): A list of God objects.
        goods (List[Good]): A list of Good objects.
        numerals (List[Numeral]): A list of Numeral objects.

    Returns:
        List[Card]: A list of Card objects.
    """
    cards = db.get_concordia_cards()
    cards_list = []
    for card in cards:
        if card['CARD_NAME'] != 'SPECIALIST':
            cards_list.append(data_to_card(card, gods, goods, numerals))
    return cards_list


def fill_display_area(goods: List[Good]) -> List[DisplayArea]:
    """
    Returns a list of DisplayArea objects filled with data from the database.

    Args:
        goods (List[Good]): A list of Good objects to be used to fill the
            DisplayArea objects.

    Returns:
        List[DisplayArea]: A list of DisplayArea objects filled with data from
            the database.
    """
    display_areas = db.get_concordia_display_area()
    display_areas_list = []
    for display_area in display_areas:
        display_areas_list.append(data_to_display_area(display_area, goods))
    return display_areas_list
