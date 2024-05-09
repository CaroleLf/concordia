import unittest
from CONCORDIA.TEST.data_factory import DataFactory
from CONCORDIA.METIER.player import Player


class MyTestCase(unittest.TestCase):
    def test_get_good_counts(self):
        player = Player(1, "red", 0, DataFactory.create_default_good(), [], [], [], [])
        self.assertEqual({'brick': 1, 'food': 1, 'tool': 1, 'wine': 1, 'cloth': 1},
                         player.get_good_counts())
        player.player_goods.pop(0)
        self.assertEqual({'food': 1, 'tool': 1, 'wine': 1, 'cloth': 1},
                         player.get_good_counts())
        player.player_goods.extend(DataFactory.create_default_good())
        self.assertEqual({'brick': 1, 'food': 2, 'tool': 2, 'wine': 2, 'cloth': 2},
                         player.get_good_counts())
        player.player_goods = []
        self.assertEqual({},
                         player.get_good_counts())

    def test_get_good_names(self):
        player = Player(1, "red", 0, DataFactory.create_default_good(), [], [], [], [])
        self.assertEqual(['brick', 'food', 'tool', 'wine', 'cloth'], player.get_good_names())
        player.player_goods.pop(0)
        player.player_goods.pop(0)
        self.assertEqual(['tool', 'wine', 'cloth'], player.get_good_names())
        player.player_goods = []
        self.assertEqual([], player.get_good_names())

    def test_get_good_by_name(self):
        player = Player(1, "red", 0, DataFactory.create_default_good(), [], [], [], [])
        self.assertEqual(player.player_goods[0], player.get_good_by_name('brick'))
        self.assertEqual(player.player_goods[4], player.get_good_by_name('cloth'))
        player.player_goods = []
        self.assertEqual(None, player.get_good_by_name('brick'))

    def test_get_good_count(self):
        player = Player(1, "red", 0, DataFactory.create_default_good(), [], [], [], [])
        self.assertEqual(1, player.get_good_count('brick'))
        player.player_goods.extend(DataFactory.create_default_good())
        self.assertEqual(2, player.get_good_count('cloth'))
        player.player_goods = []
        self.assertEqual(0, player.get_good_count('food'))

    def test_remove_good(self):
        player = Player(1, "red", 0, DataFactory.create_default_good(), [], [], [], [])
        self.assertTrue(player.remove_goods('brick', 1))
        self.assertFalse(player.remove_goods('brick', 1))
        player.player_goods = []
        self.assertFalse(player.remove_goods('cloth', 2))

    def test_add_goods(self):
        goods = DataFactory.create_default_good()
        player = Player(1, "red", 0, [], [], [], [], [])
        player.add_goods(goods[0], 2)
        self.assertEqual(2, player.get_good_count('brick'))

    def test_have_prafectus_magnus(self):
        cards = DataFactory.create_default_cards()
        player = Player(1, "red", 0, [], [], cards, [], [])
        self.assertEqual(False, player.have_prafectus_magnus())
