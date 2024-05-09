import random
import unittest

from CONCORDIA.METIER.BOARD.house import House
from CONCORDIA.METIER.game import Game
from CONCORDIA.METIER.player import Player
from CONCORDIA.TEST.data_factory import DataFactory


class TestGame(unittest.TestCase):
    def test_find_player_by_color(self):
        player_blue = Player(1, "blue", 0, [], [], [], [], [])
        player_green = Player(1, "green", 0, [], [], [], [], [])
        player_purple = Player(1, "purple", 0, [], [], [], [], [])
        player_red = Player(1, "red", 0, [], [], [], [], [])
        players = [player_green, player_purple, player_blue, player_red]
        g = DataFactory.create_default_game()[0]

        self.assertNotEqual(g.find_player_by_color("blue", players), player_red)
        self.assertEqual(g.find_player_by_color("green", players), player_green)
        self.assertEqual(g.find_player_by_color("purple", players), player_purple)
        self.assertEqual(g.find_player_by_color("red", players), player_red)

    def test_initialize_shop(self):

        g = DataFactory.create_default_game()[0]
        g.initialize_shop()
        self.assertEqual(6, len(g.game_shop_available))

    def test_get_next_card(self):
        g, card_expected = DataFactory.create_default_game()
        self.assertEqual(card_expected, g.get_next_card())

    def test_define_bonus_token_province(self):
        g = DataFactory.create_default_game()[0]
        self.assertEqual(g.game_map.map_coll_provinces[0].bonus_token, None)
        self.assertEqual(g.game_map.map_coll_provinces[1].bonus_token, None)
        self.assertEqual(g.game_map.map_coll_provinces[2].bonus_token, None)
        g.define_bonus_token_province()
        self.assertNotEqual(g.game_map.map_coll_provinces[0].bonus_token, None)
        self.assertNotEqual(g.game_map.map_coll_provinces[1].bonus_token, None)
        self.assertNotEqual(g.game_map.map_coll_provinces[2].bonus_token, None)

    def test_replace_card(self):
        g = DataFactory.create_default_game()[0]
        g.initialize_shop()
        for da, card in g.game_shop_available.items():
            g.game_shop_available[da] = None
            self.assertEqual(g.game_shop_available[da], None)
        g.replace_card()
        for da, card in g.game_shop_available.items():
            self.assertNotEqual(g.game_shop_available[da], None)

    def test_empty_game_shop_available(self):
        g: Game = DataFactory.create_default_game()[0]
        for d in g.game_display_area:
            g.game_shop_available[d] = None
        self.assertEqual(True, g.empty_game_shop_available())
        g.initialize_shop()
        self.assertEqual(False, g.empty_game_shop_available())

    def test_define_winner(self):
        g: Game = DataFactory.create_default_game()[0]
        player_score = {}
        max: dict[Player, int] = None
        for p in g.game_players:
            score = random.randint(5, 100)
            if max is None or score > player_score[max]:
                max = p
            player_score[p] = score
        self.assertEqual(g.define_winner(player_score), max)

    def test_end_game(self):
        g: Game = DataFactory.create_default_game()[0]
        p = g.game_players[0]
        for i in range(15):
            g.game_map.map_coll_houses.append(House(p_house_city=None, p_house_player=p))
        self.assertEqual(True, g.end_game(p))
        self.assertEqual(False, g.end_game(g.game_players[1]))
