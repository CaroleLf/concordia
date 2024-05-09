import unittest

from CONCORDIA.METIER.BOARD.map import Map
from CONCORDIA.METIER.BOARD.city import City
from CONCORDIA.METIER.numeral import Numeral
from CONCORDIA.METIER.sdo_point import SDOPoint
from CONCORDIA.METIER.BOARD.province import Province
from CONCORDIA.METIER.LINES.line import Line
from CONCORDIA.METIER.LINES.way import Way
from CONCORDIA.METIER.good import Good


class TestCreateMap(unittest.TestCase):
    def test_create_map(self):
        self.anvil = Good(p_good_name="Anvil",
                          p_good_price=10, p_good_color="Gray")

        # Given
        map_name = "Italia"
        map_min_player = 2
        map_max_player = 5
        map_capital = City("Roma", "A", True, SDOPoint(41, 12), None, [])
        city_1 = City("Burdigala", "A", False, SDOPoint(44, 0), None, [])
        city_2 = City("Massilia", "B", False, SDOPoint(43, 5), None, [])
        city_3 = City("Narbo", "B", False, SDOPoint(43, 3), None, [])
        province_1 = Province("Aquitania", Numeral(1, "I"), [city_1], SDOPoint(44, 0), None)
        province_2 = Province("Narbonensis", Numeral(2, "II"), [city_2, city_3], SDOPoint(43, 5), None)
        province_3 = Province("Liguria", Numeral(3, "III"), [], SDOPoint(47, 0), None)
        map_coll_provinces = [province_1, province_2, province_3]
        map_coordinates = SDOPoint(50, 12)
        type_line_land = Way("Land", "brown")
        type_line_sea = Way("Sea", "blue")
        line_1 = Line(city_1, city_2, None, type_line_land)
        line_2 = Line(city_2, city_3, None, type_line_sea)
        line_3 = Line(city_3, city_1, None, type_line_land)
        map_coll_line = [line_1, line_2, line_3]

        test_map = Map(map_name,
                       map_min_player,
                       map_max_player,
                       map_capital,
                       map_coll_provinces,
                       map_coordinates,
                       map_coll_line)

        self.assertEqual(test_map.map_name, "Italia")
        self.assertEqual(test_map.map_min_player, 2)
        self.assertEqual(test_map.map_max_player, 5)
        self.assertEqual(len(test_map.map_coll_line), 3)
        self.assertEqual(test_map.map_capital.city_name, "Roma")
        self.assertEqual(test_map.map_capital.city_roman_char, "A")
        self.assertTrue(test_map.map_capital.city_is_capital)
        self.assertEqual(test_map.map_capital.city_coordinates.sdo_point_x, 41)
        self.assertEqual(test_map.map_capital.city_coordinates.sdo_point_y, 12)
        self.assertIsNone(test_map.map_capital.city_good)
        self.assertEqual(test_map.map_capital.city_colonists, [])
        self.assertEqual(len(test_map.map_coll_provinces), 3)
        self.assertEqual(test_map.map_coordinates.sdo_point_x, 50)
        self.assertEqual(test_map.map_coordinates.sdo_point_y, 12)
        self.assertEqual(test_map.map_coll_line, [line_1, line_2, line_3])
