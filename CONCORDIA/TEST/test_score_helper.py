import unittest

from CONCORDIA.HELPER.score_helper import (calculate_score_for_jupiter, calculate_score_for_vesta,
                                           calculate_score_for_saturne, calculate_score_for_mercurius,
                                           calculate_score_for_mars, calculate_score_for_minerva)
from CONCORDIA.METIER.BOARD.house import House
from CONCORDIA.TEST.data_factory import DataFactory


class TestScoreHelper(unittest.TestCase):
    def test_calculate_score_for_vesta(self):
        players = DataFactory.create_default_player()
        score = calculate_score_for_vesta(players[0])
        self.assertEqual(score, 4)

    def test_calculate_score_for_jupiter(self):
        players = DataFactory.create_default_player()
        map = DataFactory.create_default_map()
        map.map_coll_houses = [House(map.map_coll_provinces[0].province_coll_citys[0], players[0]),
                               House(map.map_coll_provinces[0].province_coll_citys[1], players[0])]
        score = calculate_score_for_jupiter(players[0], map)
        self.assertEqual(score, 1)

    def test_calculate_score_for_saturne(self):
        players = DataFactory.create_default_player()
        map = DataFactory.create_default_map()
        map.map_coll_houses = [House(map.map_coll_provinces[0].province_coll_citys[0], players[0]),
                               House(map.map_coll_provinces[0].province_coll_citys[1], players[0])]
        score = calculate_score_for_saturne(players[0], map)
        self.assertEqual(score, 4)

    def test_calculate_score_for_mercurius(self):
        players = DataFactory.create_default_player()
        map = DataFactory.create_default_map()
        map.map_coll_houses = [House(map.map_coll_provinces[0].province_coll_citys[0], players[0]),
                               House(map.map_coll_provinces[0].province_coll_citys[1], players[0])]
        score = calculate_score_for_mercurius(players[0], map)
        self.assertEqual(score, 4)

    def test_calculate_score_for_mars(self):
        players = DataFactory.create_default_player()
        score = calculate_score_for_mars(players[0])
        self.assertEqual(score, 4)

    def test_calculate_score_for_minerva(self):
        player = DataFactory.create_default_player()
        goods = DataFactory.create_default_good()
        map = DataFactory.create_default_map()
        map.map_coll_houses = [House(map.map_coll_provinces[0].province_coll_citys[0], player[0]),
                               House(map.map_coll_provinces[0].province_coll_citys[1], player[0])]
        score = calculate_score_for_minerva(player[0], map, goods[2])
        self.assertEqual(score, 5)
