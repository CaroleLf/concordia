import unittest
from unittest.mock import patch

from CONCORDIA.METIER.CARDS.consul import Consul
from CONCORDIA.METIER.CARDS.prefect import Prefect
from CONCORDIA.METIER.CARDS.senator import Senator
from CONCORDIA.METIER.CARDS.colonist import Colonist
from CONCORDIA.METIER.CARDS.architect import Architect

from CONCORDIA.METIER.god import God
from CONCORDIA.METIER.game import Game
from CONCORDIA.METIER.good import Good
from CONCORDIA.METIER.player import Player
from CONCORDIA.METIER.numeral import Numeral
from CONCORDIA.METIER.sdo_point import SDOPoint
from CONCORDIA.METIER.display_area import DisplayArea

from CONCORDIA.METIER.BOARD.map import Map
from CONCORDIA.METIER.BOARD.city import City
from CONCORDIA.METIER.BOARD.house import House
from CONCORDIA.METIER.BOARD.province import Province
from CONCORDIA.METIER.BOARD.bonus_token import BonusToken

from CONCORDIA.METIER.CARDS.tribune import Tribune
from CONCORDIA.METIER.CARDS.mercator import Mercator
from CONCORDIA.METIER.CARDS.diplomat import Diplomat
from CONCORDIA.METIER.CARDS.specialist import Specialist

from CONCORDIA.METIER.LINES.way import Way
from CONCORDIA.METIER.LINES.line import Line

from CONCORDIA.METIER.COLONISTS.colonist_pawn import ColonistPawn


class TestCards(unittest.TestCase):

    def setUp(self):
        self.tool = Good(p_good_name="tool",
                         p_good_price=10, p_good_color="Gray")
        self.wine = Good(p_good_name="wine",
                         p_good_price=5, p_good_color="Red")
        self.food = Good(p_good_name="food",
                         p_good_price=3, p_good_color="Yellow")
        self.cloth = Good(p_good_name="cloth",
                          p_good_price=8, p_good_color="Blue")
        self.brick = Good(p_good_name="brick",
                          p_good_price=1, p_good_color="Bordeaux")

        self.colonist_sea = ColonistPawn(p_colonist_color="Green", p_colonist_type="Land")
        self.colonist_land = ColonistPawn(p_colonist_color="Green", p_colonist_type="Land")

        self.colonist_city = ColonistPawn(p_colonist_color="Red", p_colonist_type="Land")
        self.colonist_line = ColonistPawn(p_colonist_color="Red", p_colonist_type="Sea")

        self.player = Player(
            p_player_wallet=3,
            p_player_color="Red",
            p_player_score=0,
            p_player_goods=[self.tool, self.wine, self.food, self.cloth, self.brick],
            p_player_played_cards=[],
            p_player_playable_cards=[],
            p_player_colonists_board=[self.colonist_city, self.colonist_line],
            p_player_colonists_inventory=[]
        )

        self.player2 = Player(
            p_player_wallet=5,
            p_player_color="Green",
            p_player_score=0,
            p_player_goods=[self.wine, self.food, self.food, self.tool],
            p_player_played_cards=[],
            p_player_playable_cards=[],
            p_player_colonists_board=[],
            p_player_colonists_inventory=[]
        )

        self.player3 = Player(
            p_player_wallet=5,
            p_player_color="Green",
            p_player_score=0,
            p_player_goods=[
                self.tool, self.tool, self.tool, self.tool,
                self.food, self.food, self.food
            ],
            p_player_played_cards=[],
            p_player_playable_cards=[],
            p_player_colonists_board=[],
            p_player_colonists_inventory=[
                self.colonist_land,
                self.colonist_sea, self.colonist_sea,
                self.colonist_sea, self.colonist_sea
            ]

        )

        map_name = "Italia"
        map_min_player = 2
        map_max_player = 5
        map_capital = City("Roma", "B", True, SDOPoint(41, 12), None, [])
        self.city_1 = City("City1", "A", False, SDOPoint(44, 0), self.tool, [self.colonist_city])
        city_2 = City("City2", "A", False, SDOPoint(43, 1), self.wine, [])
        city_3 = City("City3", "A", False, SDOPoint(43, 2), self.wine, [])
        city_4 = City("City4", "A", False, SDOPoint(44, 3), self.food, [])
        city_5 = City("City5", "B", False, SDOPoint(43, 4), self.wine, [])
        city_6 = City("City6", "B", False, SDOPoint(43, 5), self.food, [])
        city_7 = City("City7", "C", False, SDOPoint(44, 6), self.cloth, [])
        city_8 = City("City8", "C", False, SDOPoint(43, 7), self.cloth, [])
        city_9 = City("City9", "C", False, SDOPoint(43, 8), self.food, [])
        self.bonus_token: BonusToken = BonusToken(2, self.tool)
        province_1 = Province("Aquitania", Numeral(1, "I"),
                              [self.city_1, city_2, city_3, city_4],
                              SDOPoint(44, 0), self.bonus_token)
        province_2 = Province("Narbonensis", Numeral(2, "II"),
                              [map_capital, city_5, city_6],
                              SDOPoint(43, 5), self.bonus_token)
        province_3 = Province("Liguria", Numeral(3, "III"),
                              [city_7, city_8, city_9],
                              SDOPoint(47, 0), self.bonus_token)
        map_coll_provinces = [province_1, province_2, province_3]
        map_coordinates = SDOPoint(50, 12)
        type_line_land = Way("Land", "brown")
        type_line_sea = Way("Sea", "blue")
        line_1 = Line(self.city_1, city_2, None, type_line_land)
        line_2 = Line(self.city_1, city_3, None, type_line_sea)
        line_3 = Line(self.city_1, city_4, None, type_line_land)
        self.line_4 = Line(self.city_1, map_capital, None, type_line_land)
        line_5 = Line(map_capital, city_5, None, type_line_land)
        line_6 = Line(map_capital, city_7, self.colonist_line, type_line_sea)
        line_7 = Line(city_7, city_6, None, type_line_sea)
        line_8 = Line(city_7, city_9, None, type_line_land)
        line_9 = Line(city_7, city_8, None, type_line_sea)
        line_10 = Line(city_5, city_7, None, type_line_sea)
        map_coll_line = [line_1, line_2, line_3, self.line_4,
                         line_5, line_6, line_7, line_8, line_9, line_10]
        # house_1 = House(self.city_1, self.player)
        house_2 = House(city_2, self.player)
        house_3 = House(city_3, self.player)

        self.test_map = Map(map_name,
                            map_min_player,
                            map_max_player,
                            map_capital,
                            map_coll_provinces,
                            map_coordinates,
                            map_coll_line)
        self.test_map.map_coll_houses = [house_2, house_3]
        self.game = Game(
            p_game_map=self.test_map,
            p_game_players=[self.player],
            p_game_goods=[],
            p_game_display_area=[],
            p_game_shop=[]
        )

        self.card_god = God(
            p_god_name="Jesus",
            p_god_example="Jesus",
            p_god_significance="g",
            p_god_reward="f",
            p_god_victory_points=4
        )

        self.display_area = DisplayArea(
            p_display_area_any_good_required=True,
            p_display_area_n_goods=1,
            p_display_area_position=1,
            p_display_area_good=self.wine
        )

        self.display_area2 = DisplayArea(
            p_display_area_any_good_required=True,
            p_display_area_n_goods=2,
            p_display_area_position=2,
            p_display_area_good=self.wine
        )

        self.numeral = Numeral(
            p_numeral_arabic=5,
            p_numeral_roman="5"
        )

    def test_mercator_card_action(self):
        card = Mercator(
            p_card_name="Mercator",
            p_card_description="Mercator",
            p_card_example="Mercator",
            p_card_god=self.card_god,
            p_card_for_sale_deck=[self.numeral],
            p_card_goods_cost=[self.tool]
        )
        self.player.player_playable_cards.append(card)
        last_added_card = self.player.player_playable_cards[-1]
        last_added_card.sell(self.player, self.wine, 1)
        self.assertEqual(self.player.player_wallet, 8)

        self.assertEqual(self.player.player_goods, [
                         self.tool, self.food, self.cloth, self.brick])
        card.buy(self.player, self.cloth, 1)
        self.assertEqual(self.player.player_wallet, 0)
        self.assertEqual(self.player.player_goods, [
                         self.tool, self.food, self.cloth, self.brick, self.cloth])

    def test_diplomat_card_action(self):
        card = Diplomat(
            p_card_name="Diplomat",
            p_card_description="Diplomat",
            p_card_example="Diplomat",
            p_card_god=self.card_god,
            p_card_for_sale_deck=[self.numeral],
            p_card_goods_cost=[self.cloth]
        )
        card_m = Mercator(
            p_card_name="Mercator",
            p_card_description="Mercator",
            p_card_example="Mercator",
            p_card_god=self.card_god,
            p_card_for_sale_deck=[self.numeral],
            p_card_goods_cost=[self.tool]
        )

        self.player.player_playable_cards.append(card)
        self.player2.player_played_cards.append(card_m)

        self.assertEqual(len(self.player.player_playable_cards), 1)
        self.assertEqual(len(self.player.player_played_cards), 0)
        last_added_card = self.player.player_playable_cards[-1]
        last_added_card.play_last_card_of_player(
            self.player, self.player2, self.game)

        self.assertEqual(len(self.player.player_playable_cards), 2)
        self.assertEqual(len(self.player.player_played_cards), 0)

    def test_specialist_card_action(self):
        card = Specialist(
            p_card_name="Specialist",
            p_card_description="Specialist",
            p_card_example="Specialist",
            p_card_god=self.card_god,
            p_card_for_sale_deck=[self.numeral],
            p_card_goods_cost=[self.wine]
        )

        card.speciality = self.wine

        self.player.player_playable_cards.append(card)
        self.assertEqual(len(self.player.player_goods), 5)
        last_added_card = self.player.player_playable_cards[-1]
        last_added_card.card_action(self.player, self.test_map)
        self.assertEqual(len(self.player.player_goods), 7)

    def test_tribune_card_action(self):
        card = Tribune(
            p_card_name="Tribune",
            p_card_description="Tribune",
            p_card_example="Tribune",
            p_card_god=self.card_god,
            p_card_for_sale_deck=[],
            p_card_goods_cost=[]
        )

        self.player3.player_playable_cards.append(card)
        last_added_card = self.player3.player_playable_cards[-1]
        last_added_card.buy_colonist(self.player3, self.game.game_map, self.colonist_sea)
        last_added_card.choose_colonist(self.player3, self.game.game_map, "land")
        last_added_card.choose_colonist(self.player3, self.game.game_map, "cancel")
        last_added_card.choose_colonist_type(self.player3, self.game.game_map, 'y')
        last_added_card.choose_colonist_type(self.player3, self.game.game_map, 'n')
        last_added_card.buy_colonist(self.player3, self.game.game_map, self.colonist_land)

        self.assertEqual(3, len(self.player3.player_colonists_board))

    def test_architect_card_action(self):
        card = Architect(
            p_card_name="Architect",
            p_card_description="Architect",
            p_card_example="Architect",
            p_card_god=self.card_god,
            p_card_for_sale_deck=[self.numeral],
            p_card_goods_cost=[self.wine]
        )

        self.player.player_playable_cards.append(card)
        last_added_card = self.player.player_playable_cards[-1]
        test = last_added_card.get_all_possible_movement_for_one_colonist(
            self.colonist_city, self.game)
        self.assertEqual(len(test), 3)
        test = last_added_card.get_all_possible_movement_for_one_colonist(
            self.colonist_line, self.game)
        self.assertEqual(len(test), 3)
        self.assertEqual(len(self.player.player_goods), 5)
        self.assertEqual(self.player.player_wallet, 3)
        self.player.purchase_house(self.city_1)
        self.assertEqual(len(self.player.player_goods), 3)
        self.assertEqual(self.player.player_wallet, 0)
        # On peut pas tester le fait que ça ajout bien une house dans le map mais c'est bien le cas

    def test_prefect_card_action(self):
        card = Prefect(
            p_card_name="Prefect",
            p_card_description="Prefect",
            p_card_example="Prefect",
            p_card_god=self.card_god,
            p_card_for_sale_deck=[self.numeral],
            p_card_goods_cost=[self.wine]
        )
        self.player.player_playable_cards.append(card)
        provisoire_province = self.test_map.get_province_by_name("AQUITANIA")
        last_added_card = self.player.player_playable_cards[-1]
        self.assertEqual(len(self.player.player_goods), 5)
        last_added_card.collect_goods(self.player, self.test_map, provisoire_province)
        self.assertEqual(len(self.player.player_goods), 7)
        last_added_card.collect_bonus_token(self.bonus_token, self.player)
        self.assertEqual(len(self.player.player_goods), 8)
        self.bonus_token.returned()
        self.assertEqual(self.player.player_wallet, 3)
        last_added_card.collect_bonus_cash([provisoire_province], self.player)
        self.assertEqual(self.player.player_wallet, 5)

    def test_senator_card_action(self):
        card = Senator(
            p_card_name="Senator",
            p_card_description="Senator",
            p_card_example="Senator",
            p_card_god=self.card_god,
            p_card_for_sale_deck=[self.numeral],
            p_card_goods_cost=[self.wine]
        )
        card2 = Prefect(
            p_card_name="Prefect",
            p_card_description="Prefect",
            p_card_example="Prefect",
            p_card_god=self.card_god,
            p_card_for_sale_deck=[self.numeral],
            p_card_goods_cost=[self.food]
        )
        card3 = Architect(
            p_card_name="Architect",
            p_card_description="Architect",
            p_card_example="Architect",
            p_card_god=self.card_god,
            p_card_for_sale_deck=[self.numeral],
            p_card_goods_cost=[self.wine]
        )
        card4 = Diplomat(
            p_card_name="Diplomat",
            p_card_description="Diplomat",
            p_card_example="Diplomat",
            p_card_god=self.card_god,
            p_card_for_sale_deck=[self.numeral],
            p_card_goods_cost=[self.wine]
        )
        self.player.player_playable_cards.append(card)
        last_added_card = self.player.player_playable_cards[-1]
        self.game.game_shop_available = {self.display_area: card2, self.display_area2: card3}
        self.game.game_shop = {"I": [card4]}
        self.assertEqual(len(self.player.player_goods), 5)

        last_added_card.buy_card(self.player, self.game, 2)
        self.assertEqual(len(self.player.player_goods), 4)
        self.game.replace_card()

    def test_get_sestertii_from_colonists(self):
        colonist_card = Colonist(
            "Colonist Card",
            "Description of Colonist Card",
            True,
            "Colonist God",
            "I",
            p_card_goods_cost=[Good("food",
                                    1,
                                    "red")])

        test_player = Player(0,
                             p_player_color="red",
                             p_player_goods=[],
                             p_player_colonists_board=[],
                             p_player_colonists_inventory=[],
                             p_player_playable_cards=[colonist_card],
                             p_player_played_cards=[],
                             p_player_score=0)
        initial_wallet = test_player.player_wallet

        # Ajoutez quelques colonistes au joueur
        test_player.add_colonist(ColonistPawn("red", "land"))
        test_player.add_colonist(ColonistPawn("red", "land"))

        # Sélectionnez "n" pour ne pas placer de colonistes
        with patch('builtins.input', side_effect=['n']):
            colonist_card.card_action(test_player, [])

        # Vérifiez que le portefeuille du joueur a été mis à jour correctement
        expected_wallet = initial_wallet
        expected_wallet += 5 + len(test_player.player_colonists_board)
        self.assertEqual(test_player.player_wallet, expected_wallet)

        initial_wallet = test_player.player_wallet

        # Ajoutez quelques colonistes au joueur
        test_player.add_colonist(ColonistPawn("red", "land"))
        test_player.add_colonist(ColonistPawn("b", "water"))
        expected_wallet = initial_wallet
        expected_wallet += 5 + len(test_player.player_colonists_board)
        with patch('builtins.input', side_effect=['n']):
            colonist_card.card_action(test_player, [])
        self.assertEqual(test_player.player_wallet, expected_wallet)

    def test_place_colonists(self):
        colonist_card = Colonist(
            "Colonist Card",
            "Description of Colonist Card",
            True,
            "Colonist God",
            "I",
            p_card_goods_cost=[Good("food",
                                    p_good_price=1,
                                    p_good_color="red")])
        colonist_type = "land"

        city1 = City("City1",
                     "I",
                     False,
                     SDOPoint(1, 1),
                     Good("food", 1, p_good_color="red"),
                     [ColonistPawn("red", colonist_type)])

        test_player = Player(0,
                             p_player_color="red",
                             p_player_goods=[],
                             p_player_colonists_inventory=[],
                             p_player_colonists_board=[ColonistPawn("red", colonist_type)],
                             p_player_playable_cards=[colonist_card],
                             p_player_played_cards=[],
                             p_player_score=0)
        test_player.player_goods.append(Good("food", 1, p_good_color="red"))
        test_player.player_goods.append(Good("tool", 1, p_good_color="red"))

        house1 = House(city1, test_player)

        with patch('builtins.input', side_effect=['y', 'City1']):
            colonist_card.card_action(test_player, [house1])

        # Vérifiez que le coloniste a été placé dans la ville correcte
        city_colonist = house1.house_city.city_colonists[0]
        self.assertEqual(len(house1.house_city.city_colonists), 1)
        self.assertEqual(city_colonist.colonist_color, "red")
        self.assertEqual(city_colonist.colonist_type, colonist_type)
        self.assertEqual(len(test_player.player_goods), 2)
        self.assertEqual(len(test_player.player_colonists_board), 1)

        # Vérifiez que le joueur ne peut pas placer de coloniste
        # s'il n'en a plus
        with patch('builtins.input', side_effect=['y', 'City1']):
            colonist_card.card_action(test_player, [house1])
        self.assertEqual(len(house1.house_city.city_colonists), 1)

        # Vérifiez que le joueur ne peut pas placer de coloniste
        # s'il n'a pas assez de nourriture
        test_player.player_colonists_board.append(ColonistPawn("red", colonist_type))
        with patch('builtins.input', side_effect=['y', 'City1']):
            colonist_card.card_action(test_player, [house1])
        self.assertEqual(len(house1.house_city.city_colonists), 1)

        # Vérifiez que le joueur ne peut pas placer de coloniste
        # s'il n'a pas assez d'outils
        test_player.player_goods.append(Good("food", 1, p_good_color="red"))
        with patch('builtins.input', side_effect=['y', 'City1']):
            colonist_card.card_action(test_player, [house1])
        self.assertEqual(len(house1.house_city.city_colonists), 1)

    def test_consul_card_action(self):
        card = Consul(
            p_card_name="Consul",
            p_card_description="Consul",
            p_card_example="Consul",
            p_card_god=self.card_god,
            p_card_for_sale_deck=[self.numeral],
            p_card_goods_cost=[self.wine]
        )
        card2 = Prefect(
            p_card_name="Prefect",
            p_card_description="Prefect",
            p_card_example="Prefect",
            p_card_god=self.card_god,
            p_card_for_sale_deck=[self.numeral],
            p_card_goods_cost=[self.wine]
        )
        self.player.player_playable_cards.append(card)
        last_added_card = self.player.player_playable_cards[-1]
        self.game.game_shop_available = {self.display_area: card2}
        self.assertEqual(5, len(self.player.player_goods))
        self.assertTrue(last_added_card.buyable(self.player, last_added_card.get_good_counts(card2.card_goods_cost)))
        last_added_card.buy_card(self.game, self.player, self.display_area)
        self.assertEqual(4, len(self.player.player_goods))
