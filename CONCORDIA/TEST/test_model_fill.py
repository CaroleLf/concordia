import unittest

from CONCORDIA.DAL.model_fill import data_to_city, data_to_sdo_point, \
    data_to_province, data_to_way, data_to_line, \
    data_to_map, data_to_god, data_to_card, data_to_numeral, \
    data_to_display_area
from CONCORDIA.TEST.data_factory import DataFactory


class TestModelFill(unittest.TestCase):
    def test_data_to_sdo_point(self):
        data = {
            "X": 129.0,
            "Y": 36.0
        }
        sdo_point = data_to_sdo_point(data)
        self.assertEqual(sdo_point.sdo_point_x, 129.0)
        self.assertEqual(sdo_point.sdo_point_y, 36.0)

    def test_data_to_city(self):
        data = {
            "CITY_COORDINATES": {
                "X": 129.0,
                "Y": 36.0,
                "Z": None
            },
            "CITY_NAME": "LONDINIVM",
            "CITY_ROMAN_CHAR": "A"
        }
        city = data_to_city(data)
        self.assertEqual(city.city_name, "LONDINIVM")
        self.assertEqual(city.city_roman_char, "A")
        self.assertEqual(city.city_is_capital, False)
        self.assertEqual(city.city_coordinates.sdo_point_x, 129.0)
        self.assertEqual(city.city_coordinates.sdo_point_y, 36.0)

    def test_data_to_city_capital(self):
        data = {
            "CITY_COORDINATES": {
                "X": 129.0,
                "Y": 36.0,
                "Z": None
            },
            "CITY_NAME": "LONDINIVM",
            "CITY_ROMAN_CHAR": "A"
        }
        city = data_to_city(data, True)
        self.assertEqual(city.city_name, "LONDINIVM")
        self.assertEqual(city.city_roman_char, "A")
        self.assertEqual(city.city_is_capital, True)
        self.assertEqual(city.city_coordinates.sdo_point_x, 129.0)
        self.assertEqual(city.city_coordinates.sdo_point_y, 36.0)

    def test_data_to_province(self):
        numerals = DataFactory.create_default_numeral()
        data = {
            "PROVINCE_CITY": [
                {
                    "CITY_COORDINATES": {
                        "X": 129.0,
                        "Y": 36.0,
                        "Z": None
                    },
                    "CITY_NAME": "LONDINIVM",
                    "CITY_ROMAN_CHAR": "A"
                },
                {
                    "CITY_COORDINATES": {
                        "X": 86.0,
                        "Y": 59.0,
                        "Z": None
                    },
                    "CITY_NAME": "ISCA DVMNONIORVM",
                    "CITY_ROMAN_CHAR": "A"
                }
            ],
            "PROVINCE_COORDINATES": {
                "X": 24.0,
                "Y": 46.0,
                "Z": None
            },
            "PROVINCE_NAME": "BRITANNIA",
            "PROVINCE_ROMAN_NUM": "I"
        }
        province = data_to_province(data, numerals)
        self.assertEqual(province.province_name, "BRITANNIA")
        self.assertEqual(province.province_roman_num.numeral_roman, "I")
        self.assertEqual(province.province_roman_num.numeral_arabic, 1)
        self.assertEqual(province.province_coordinates.sdo_point_x, 24.0)
        self.assertEqual(province.province_coordinates.sdo_point_y, 46.0)
        self.assertEqual(len(province.province_coll_citys), 2)
        self.assertEqual(
            province.province_coll_citys[0].city_name, "LONDINIVM")
        self.assertEqual(
            province.province_coll_citys[1].city_name, "ISCA DVMNONIORVM")

    def test_data_to_way(self):
        data = {
            "WAY_COLOR": "brown",
            "WAY_NAME": "land"
        }
        way = data_to_way(data)
        self.assertEqual(way.way_name, "land")
        self.assertEqual(way.way_color, "brown")

    def test_data_to_line(self):
        data = {
            "LINE_CITY_1": "BURDIGALA",
            "LINE_CITY_2": "MASSILIA",
            "LINE_WAY": "land"
        }
        citys = DataFactory.create_default_city()
        ways = DataFactory.create_default_way()
        line = data_to_line(data, citys, ways)
        self.assertEqual(line.line_city_1.city_name, "BURDIGALA")
        self.assertEqual(line.line_city_2.city_name, "MASSILIA")
        self.assertEqual(line.line_way.way_name, "land")
        self.assertEqual(line.line_way.way_color, "brown")

    def test_data_to_map(self):
        data = {
            "MAP_MAX_COORDINATES": {
                "X": 692.0,
                "Y": 373.0,
                "Z": None
            },
            "MAP_MAX_N_PLAYERS": 5.0,
            "MAP_MIN_N_PLAYERS": 3.0,
            "MAP_NAME": "Imperium"
        }
        capital = DataFactory.create_default_city()[0]
        provinces = DataFactory.create_default_province()
        lines = DataFactory.create_default_line()
        map = data_to_map(data, capital, provinces, lines)
        self.assertEqual(map.map_name, "Imperium")
        self.assertEqual(map.map_min_player, 3)
        self.assertEqual(map.map_max_player, 5)
        self.assertEqual(map.map_capital.city_name, " R O M A ")
        self.assertEqual(map.map_coll_provinces[0].province_name, "BRITANNIA")
        self.assertEqual(
            map.map_coll_provinces[0].province_roman_num.numeral_roman, "I")
        self.assertEqual(
            map.map_coll_provinces[0].province_coordinates.sdo_point_x, 24.0)
        self.assertEqual(
            map.map_coll_provinces[0].province_coordinates.sdo_point_y, 46.0)
        self.assertEqual(
            map.map_coll_provinces[0].province_coll_citys[0].city_name,
            "BURDIGALA")
        self.assertEqual(
            map.map_coll_provinces[0].province_coll_citys[1].city_name,
            "MASSILIA")
        self.assertEqual(map.map_coordinates.sdo_point_x, 692.0)
        self.assertEqual(map.map_coordinates.sdo_point_y, 373.0)
        self.assertEqual(
            map.map_coll_line[0].line_city_1.city_name, " R O M A ")
        self.assertEqual(
            map.map_coll_line[0].line_city_2.city_name, "BURDIGALA")
        self.assertEqual(map.map_coll_line[0].line_way.way_name, "land")
        self.assertEqual(map.map_coll_line[0].line_way.way_color, "brown")
        self.assertEqual(
            map.map_coll_line[1].line_city_1.city_name, "BURDIGALA")
        self.assertEqual(
            map.map_coll_line[1].line_city_2.city_name, "MASSILIA")
        self.assertEqual(map.map_coll_line[1].line_way.way_name, "land")
        self.assertEqual(map.map_coll_line[1].line_way.way_color, "brown")

    def test_data_to_god(self):
        data = {
            "GOD_EXAMPLE": "Concordia example",
            "GOD_NAME": "CONCORDIA",
            "GOD_REWARD": "7 VP",
            "GOD_SIGNIFICANCE": "it's concordia god significance",
            "GOD_VICTORY_POINTS": 7.0
        }
        god = data_to_god(data)
        self.assertEqual(god.god_name, "CONCORDIA")
        self.assertEqual(god.god_example, "Concordia example")
        self.assertEqual(god.god_significance,
                         "it's concordia god significance")
        self.assertEqual(god.god_reward, "7 VP")
        self.assertEqual(god.god_victory_points, 7)

    def test_data_to_card(self):
        data = {
            "CARD_ACTION": "Produce cloth in all your corresponding houses.",
            "CARD_EXAMPLE": None,
            "CARD_FOR_SALE_COST": [
                "brick",
                "cloth"
            ],
            "CARD_FOR_SALE_DECK": [
                "II"
            ],
            "CARD_FOR_SALE_DECK_DIPLOMAT": None,
            "CARD_GOD": "MINERVA",
            "CARD_NAME": "WEAVER"
        }
        card = data_to_card(data, DataFactory.create_default_god(),
                            DataFactory.create_default_good(),
                            DataFactory.create_default_numeral())
        self.assertEqual(card.card_name, "WEAVER")
        self.assertEqual(card.card_god.god_name, "MINERVA")
        self.assertEqual(card.card_god.god_example, "Minerva example")
        self.assertEqual(card.card_description,
                         "Produce cloth in all your corresponding houses.")
        self.assertIsNone(card.card_example)
        self.assertEqual(card.card_goods_cost[0].good_name, "brick")
        self.assertEqual(card.card_goods_cost[1].good_name, "cloth")
        self.assertEqual(card.card_for_sale_deck[0].numeral_roman, "II")
        self.assertEqual(card.card_for_sale_deck[0].numeral_arabic, 2)

    def test_data_to_numeral(self):
        data = {
            "NUMERAL_ARABIC": 1.0,
            "NUMERAL_ROMAN": "I"
        }
        numeral = data_to_numeral(data)
        self.assertEqual(numeral.numeral_arabic, 1)
        self.assertEqual(numeral.numeral_roman, "I")

    def test_data_to_display_area(self):
        data = {
            "DISPLAY_AREA_ANY_GOOD_REQUIRED": "N",
            "DISPLAY_AREA_GOOD": "cloth",
            "DISPLAY_AREA_N_GOODS": 1.0,
            "DISPLAY_AREA_POSITION": 4.0
        }
        display_area = data_to_display_area(
            data, DataFactory.create_default_good())
        self.assertFalse(display_area.display_area_any_good_required)
        self.assertEqual(display_area.display_area_good.good_name, "cloth")
        self.assertEqual(display_area.display_area_n_goods, 1)
        self.assertEqual(display_area.display_area_position, 4)
