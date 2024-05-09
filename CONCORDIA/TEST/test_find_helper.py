import unittest

from CONCORDIA.HELPER.find_helper import (find_way_by_name, find_city_by_name, find_token_by_rom_char,
                                          find_god_by_name, find_good_by_name, find_numeral_by_roman,
                                          find_card_type_by_card_name)
from CONCORDIA.METIER.CARDS.colonist import Colonist
from CONCORDIA.METIER.CARDS.concordia import Concordia
from CONCORDIA.METIER.CARDS.specialist import Specialist
from CONCORDIA.TEST.data_factory import DataFactory


class TestFindHelper(unittest.TestCase):
    def test_find_way_by_name(self):
        ways = DataFactory.create_default_way()
        way = find_way_by_name(ways, "land")
        self.assertEqual(way.way_name, "land")
        self.assertEqual(way.way_color, "brown")

    def test_find_city_by_name(self):
        citys = DataFactory.create_default_city()
        city = find_city_by_name(citys, " R O M A ")
        self.assertEqual(city.city_name, " R O M A ")
        self.assertEqual(city.city_roman_char, None)
        self.assertEqual(city.city_is_capital, True)

    def test_find_token_by_rom_char(self):
        tokens = DataFactory.create_default_token()
        a_token = find_token_by_rom_char(tokens, "A")
        b_token = find_token_by_rom_char(tokens, "B")
        self.assertEqual(a_token['CITY_TOKEN_GOOD'], "brick")
        self.assertEqual(a_token['CITY_TOKEN_N_COPIES'], 2.0)
        self.assertEqual(a_token['CITY_TOKEN_ROMAN_CHAR'], "A")
        self.assertEqual(b_token['CITY_TOKEN_GOOD'], "food")
        self.assertEqual(b_token['CITY_TOKEN_N_COPIES'], 2.0)
        self.assertEqual(b_token['CITY_TOKEN_ROMAN_CHAR'], "B")

    def test_find_god_by_name(self):
        gods = DataFactory.create_default_god()
        god = find_god_by_name(gods, "CONCORDIA")
        self.assertEqual(god.god_name, "CONCORDIA")
        self.assertEqual(god.god_example, "Concordia example")
        self.assertEqual(god.god_significance, "it's concordia god significance")
        self.assertEqual(god.god_reward, "a good reward")
        self.assertEqual(god.god_victory_points, 7)

    def test_find_good_by_name(self):
        goods = DataFactory.create_default_good()
        good = find_good_by_name(goods, "brick")
        self.assertEqual(good.good_name, "brick")
        self.assertEqual(good.good_price, 3)
        self.assertEqual(good.good_color, "brown")

    def test_find_numeral_by_roman(self):
        numerals = DataFactory.create_default_numeral()
        numeral = find_numeral_by_roman(numerals, "I")
        self.assertEqual(numeral.numeral_arabic, 1)
        self.assertEqual(numeral.numeral_roman, "I")
        numeral = find_numeral_by_roman(numerals, "X")
        self.assertEqual(numeral.numeral_arabic, 10)
        self.assertEqual(numeral.numeral_roman, "X")

    def test_find_card_type_by_card_name(self):
        self.assertEqual(find_card_type_by_card_name("colonist"), Colonist)
        self.assertEqual(find_card_type_by_card_name("concordia"), Concordia)
        self.assertEqual(find_card_type_by_card_name("farmer"), Specialist)
