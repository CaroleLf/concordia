from typing import List

from CONCORDIA.METIER.BOARD.city import City
from CONCORDIA.METIER.BOARD.map import Map
from CONCORDIA.METIER.BOARD.province import Province
from CONCORDIA.METIER.CARDS.mercator import Mercator
from CONCORDIA.METIER.LINES.line import Line
from CONCORDIA.METIER.LINES.way import Way
from CONCORDIA.METIER.display_area import DisplayArea
from CONCORDIA.METIER.game import Game
from CONCORDIA.METIER.god import God
from CONCORDIA.METIER.good import Good
from CONCORDIA.METIER.numeral import Numeral
from CONCORDIA.METIER.player import Player
from CONCORDIA.METIER.sdo_point import SDOPoint
from CONCORDIA.METIER.CARDS.card import Card
from CONCORDIA.METIER.COLONISTS.colonist_pawn import ColonistPawn


class DataFactory:

    @staticmethod
    def create_default_good() -> List[Good]:
        return [Good("brick", 3, "brown"),
                Good("food", 4, "yellow"),
                Good("tool", 5, "gray"),
                Good("wine", 6, "red"),
                Good("cloth", 7, "blue")]

    @staticmethod
    def create_default_way() -> List[Way]:
        return [Way("land", "brown"),
                Way("sea", "blue"),
                Way("air", "cyan")]

    @staticmethod
    def create_default_city() -> List[City]:
        return [City(" R O M A ", None, True, SDOPoint(1, 1), None, []),
                City("BURDIGALA", "B", False, SDOPoint(1, 2), DataFactory.create_default_good()[0], []),
                City("MASSILIA", "B", False, SDOPoint(2, 2), DataFactory.create_default_good()[2], [])]

    @staticmethod
    def create_default_token() -> List:
        return [{"CITY_TOKEN_GOOD": "brick", "CITY_TOKEN_N_COPIES": 2.0,
                 "CITY_TOKEN_ROMAN_CHAR": "A"},
                {"CITY_TOKEN_GOOD": "food", "CITY_TOKEN_N_COPIES": 2.0,
                 "CITY_TOKEN_ROMAN_CHAR": "A"},
                {"CITY_TOKEN_GOOD": "tool", "CITY_TOKEN_N_COPIES": 1.0,
                 "CITY_TOKEN_ROMAN_CHAR": "A"},
                {"CITY_TOKEN_GOOD": "wine", "CITY_TOKEN_N_COPIES": 1.0,
                 "CITY_TOKEN_ROMAN_CHAR": "A"},
                {"CITY_TOKEN_GOOD": "cloth", "CITY_TOKEN_N_COPIES": 1.0,
                 "CITY_TOKEN_ROMAN_CHAR": "A"},
                {"CITY_TOKEN_GOOD": "food", "CITY_TOKEN_N_COPIES": 2.0,
                 "CITY_TOKEN_ROMAN_CHAR": "B"},
                {"CITY_TOKEN_GOOD": "brick", "CITY_TOKEN_N_COPIES": 2.0,
                 "CITY_TOKEN_ROMAN_CHAR": "B"},
                {"CITY_TOKEN_GOOD": "tool", "CITY_TOKEN_N_COPIES": 2.0,
                 "CITY_TOKEN_ROMAN_CHAR": "B"},
                {"CITY_TOKEN_GOOD": "wine", "CITY_TOKEN_N_COPIES": 1.0,
                 "CITY_TOKEN_ROMAN_CHAR": "B"},
                {"CITY_TOKEN_GOOD": "cloth", "CITY_TOKEN_N_COPIES": 1.0,
                 "CITY_TOKEN_ROMAN_CHAR": "B"}]

    @staticmethod
    def create_default_god() -> List[God]:
        return [God("CONCORDIA", "Concordia example",
                    "it's concordia god significance", "a good reward", 7),
                God("MINERVA", "Minerva example",
                    "it's minerva god significance", "a good reward", None),
                God("MARS", "Mars example", "it's mars god significance",
                    "a good reward", 2)]

    @staticmethod
    def create_default_numeral() -> List[Numeral]:
        return [Numeral(1, "I"),
                Numeral(2, "II"),
                Numeral(3, "III"),
                Numeral(4, "IV"),
                Numeral(5, "V"),
                Numeral(6, "VI"),
                Numeral(7, "VII"),
                Numeral(8, "VIII"),
                Numeral(9, "IX"),
                Numeral(10, "X"),
                Numeral(11, "XI"),
                Numeral(12, "XII")]

    @staticmethod
    def create_default_colonist_pawn() -> List[ColonistPawn]:
        return [ColonistPawn("red", "OneKindOfAColonist"),
                ColonistPawn("yellow", "OneKindOfAColonist")]

    @staticmethod
    def create_default_line() -> List[Line]:
        return [Line(DataFactory.create_default_city()[0],
                     DataFactory.create_default_city()[1], DataFactory.create_default_colonist_pawn()[0],
                     DataFactory.create_default_way()[0]),
                Line(DataFactory.create_default_city()[1],
                     DataFactory.create_default_city()[2], None,
                     DataFactory.create_default_way()[0])]

    @staticmethod
    def create_default_player() -> List[Player]:
        goods = DataFactory.create_default_good()
        player_goods = [goods[0], goods[1], goods[2], goods[3], goods[4]]
        return [Player(27, "red", 0, player_goods, [], [], DataFactory.create_default_colonist_pawn(), []),
                Player(27, "blue", 0, player_goods, [], [], DataFactory.create_default_colonist_pawn(), [])]

    @staticmethod
    def create_default_province() -> List[Province]:
        return [Province("BRITANNIA", DataFactory.create_default_numeral()[0],
                         DataFactory.create_default_city()[1:],
                         SDOPoint(24, 46), None),
                Province("FRANCE", DataFactory.create_default_numeral()[0],
                         DataFactory.create_default_city()[1:],
                         SDOPoint(24, 46), None),
                Province("SPAIN", DataFactory.create_default_numeral()[0],
                         DataFactory.create_default_city()[1:],
                         SDOPoint(24, 46), None),
                Province("ITALIA", DataFactory.create_default_numeral()[0],
                         DataFactory.create_default_city()[1:],
                         SDOPoint(24, 46), None)]

    @staticmethod
    def create_default_map() -> Map:
        return Map("Map",
                   1,
                   4,
                   DataFactory.create_default_city()[1],
                   DataFactory.create_default_province(),
                   SDOPoint(1, 1),
                   DataFactory.create_default_line())

    @staticmethod
    def create_default_display_area() -> List[DisplayArea]:
        return [DisplayArea(
            p_display_area_any_good_required=True,
            p_display_area_n_goods=1,
            p_display_area_position=1,
            p_display_area_good=DataFactory.create_default_good()[0]
        ), DisplayArea(
            p_display_area_any_good_required=True,
            p_display_area_n_goods=2,
            p_display_area_position=2,
            p_display_area_good=DataFactory.create_default_good()[0]

        ), DisplayArea(
            p_display_area_any_good_required=True,
            p_display_area_n_goods=2,
            p_display_area_position=2,
            p_display_area_good=DataFactory.create_default_good()[0]

        ), DisplayArea(
            p_display_area_any_good_required=True,
            p_display_area_n_goods=2,
            p_display_area_position=2,
            p_display_area_good=DataFactory.create_default_good()[0]

        ), DisplayArea(
            p_display_area_any_good_required=True,
            p_display_area_n_goods=2,
            p_display_area_position=2,
            p_display_area_good=DataFactory.create_default_good()[0]

        ), DisplayArea(
            p_display_area_any_good_required=True,
            p_display_area_n_goods=2,
            p_display_area_position=2,
            p_display_area_good=DataFactory.create_default_good()[0]

        )]

    @staticmethod
    def create_default_cards() -> List[Card]:
        gods = DataFactory.create_default_god()

        numerals = DataFactory.create_default_numeral()

        goods = DataFactory.create_default_good()

        cards = [
            Mercator("Carotte", "Description 1", "Example 1", gods[0], [numerals[0], numerals[2]], goods),
            Mercator("Card 2", "Description 2", "Example 2", gods[0], [numerals[1], numerals[2]], goods),
            Mercator("Card 3", "Description 3", "Example 3", gods[0], [numerals[0], numerals[4]], goods),
            Mercator("Card 4", "Description 4", "Example 4", gods[0], [numerals[4], numerals[3]], goods),
            Mercator("Card 5", "Description 5", "Example 5", gods[0], [numerals[3], numerals[1]], goods),
            Mercator("Card 4", "Description 4", "Example 4", gods[0], [numerals[4], numerals[3]], goods),
            Mercator("Card 5", "Description 5", "Example 5", gods[0], [numerals[3], numerals[1]], goods)
        ]
        return cards

    @staticmethod
    def create_default_set_cards() -> List[Card]:
        gods = DataFactory.create_default_god()

        numerals = DataFactory.create_default_numeral()
        cards = []
        goods = DataFactory.create_default_good()
        c = Mercator("Card 1", "Description 1", "Example 1", gods[0], [numerals[0], numerals[2]], goods)
        for i in range(36):
            card_copy = c
            cards.append(card_copy)
        return cards

    @staticmethod
    def create_shop(cards: List[Card]):
        cards = DataFactory.create_default_set_cards()

        shop: dict[str, List[Card]] = {"I": [cards[0], cards[1]],
                                       "II": [cards[2], cards[1]],
                                       "III": [cards[4], cards[1]],
                                       "IV": [cards[0], cards[2]],
                                       "V": [cards[3], cards[4]]}
        attended_value = cards[0]
        return shop, attended_value

    @staticmethod
    def create_default_game() -> Game:
        cards = DataFactory.create_default_set_cards()
        shop, card = DataFactory.create_shop(cards)
        g = Game(p_game_map=DataFactory.create_default_map(),
                 p_game_goods=DataFactory.create_default_good(),
                 p_game_display_area=DataFactory.create_default_display_area(),
                 p_game_players=DataFactory.create_default_player(),
                 p_game_shop=shop)
        return g, card
