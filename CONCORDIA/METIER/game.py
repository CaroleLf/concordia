from typing import List
from CONCORDIA.METIER.BOARD.map import Map
from CONCORDIA.METIER.display_area import DisplayArea
from CONCORDIA.METIER.player import Player
from CONCORDIA.METIER.good import Good
from CONCORDIA.METIER.CARDS.card import Card
from collections.abc import Mapping
from CONCORDIA.METIER.BOARD.bonus_token import BonusToken
from CONCORDIA.HELPER.score_helper import calculate_score_for_player


class Game:
    game_map: Map
    game_players: List[Player]
    game_goods: List[Good]
    game_display_area: List[DisplayArea]
    game_shop: Mapping[str, List[Card]]
    game_shop_available: Mapping[DisplayArea, Card]

    def __init__(self,
                 p_game_map: Map,
                 p_game_players: List[Player],
                 p_game_goods: List[Good],
                 p_game_display_area: List[DisplayArea],
                 p_game_shop:  Mapping[str, List[Card]]):
        self.game_map = p_game_map
        self.game_players = p_game_players
        self.game_goods = p_game_goods
        self.game_display_area = p_game_display_area
        self.game_shop_available = {}
        self.game_shop = p_game_shop

    def find_player_by_color(self, player_color: str, game_players: List[Player]) -> Player | None:
        """
        Given a player color, returns the corresponding player.

        Args:
        - player_color (str): the color of the player
        - game_players (List[Player]): the list of the player of the game

        Returns:
        - type: the player depending on the color
        """
        for player in game_players:
            if player.player_color == player_color:
                return player
        return None

    def initialize_shop(self):
        """
        Initialize the shop
        """
        for d in self.game_display_area:
            self.game_shop_available[d] = self.get_next_card()

    def get_next_card(self) -> Card | None:
        """
        Method to get the next card in the deck
        """
        for roman_numeral in self.game_shop:
            cards = self.game_shop.get(roman_numeral)
            if cards and len(cards) > 0:
                card = cards.pop(0)
                return card
        return None

    def define_bonus_token_province(self):
        """
        Method that define bonus token for a province depending on his cities
        """
        good_token = None
        bonus = None
        for province in self.game_map.map_coll_provinces:
            for city in province.province_coll_citys:
                if good_token is not None:
                    if good_token.good_price < city.city_good.good_price:
                        good_token = city.city_good
                else:
                    good_token = city.city_good
            if good_token.good_name == "cloth":
                bonus = BonusToken(bonus_sesters=1, target_good=good_token)
            else:
                bonus = BonusToken(bonus_sesters=2, target_good=good_token)
            province.bonus_token = bonus

    def replace_card(self):
        """
         Retrieve all display zones that don't have a card.
         If there's no new card to add, nothing changes in the store,
         otherwise the card is added in the right place.

        """
        keys_with_none_values = [key for key, value in self.game_shop_available.items() if value is None]
        if keys_with_none_values:
            card = self.get_next_card()
            if card is not None:
                # Create a copy of the dictionary to avoid modifying it while iterating
                temp_shop_available = dict(self.game_shop_available)

                for key_none in keys_with_none_values:
                    previous_value = None
                    for key_move, value in reversed(temp_shop_available.items()):
                        if key_none.display_area_position <= key_move.display_area_position:
                            if previous_value is not None:
                                self.game_shop_available[key_move] = previous_value  # Move the card one position right
                            if key_move.display_area_position == 7:
                                self.game_shop_available[key_move] = None
                        previous_value = value
                    for key, value in self.game_shop_available.items():
                        if value is None:
                            self.game_shop_available[key] = card
                            break

    def define_parameter_card(self, card: Card, player: Player):
        """
        Method that lauch the action of the card depending on his type
        """
        if (card.card_name == "MERCATOR" or card.card_name == "ARCHITECT" or
                card.card_name == "DIPLOMAT" or card.card_name == "SPECIALIST" or card.card_name == "CONSUL"):
            card.card_action(player, self)
        elif card.card_name == "TRIBUNE" or card.card_name == "PREFECT":
            card.card_action(player, self.game_map)
        elif card.card_name == "SENATOR":
            card.card_action(self, player)
        elif card.card_name == "COLONIST":
            houses = self.game_map.get_houses_from_player(player)
            card.card_action(player, self, houses)
        if card.card_name == "TRIBUNE":
            player.remove_card(card)

    def choose_card(self, player: Player):
        """
        Method that display all the card of the player
        """
        card_number: int = 1
        invalid_number = True
        card_selected = None
        for p in player.player_playable_cards:
            if p.card_name != "PRÆFECTVS MAGNVS":
                print(str(card_number) + " " + p.card_name)
                card_number += 1
        while invalid_number:
            try:
                number_card_selected: int = int(
                    input("Player " + player.player_color + " choose the card that you want: "))
                if 1 <= number_card_selected <= len(player.player_playable_cards):
                    card_selected = player.player_playable_cards[number_card_selected - 1]
                    self.define_parameter_card(card_selected, player)
                    invalid_number = False
                else:
                    print("Invalid card number. Please choose a valid card.")
            except ValueError:
                print("Invalid input. Please enter a valid card number (integer).")

    def empty_game_shop_available(self) -> bool:
        """
        Check if the shop available is empty
        """
        for value in self.game_shop_available.values():
            if value is not None:
                return False
        return True

    def define_winner(self, score_player: dict[Player, int]) -> Player:
        """
        Define the winner of the game
        Args:
        - score_player ( dict[str, int]): the score of all the player, key of the dict is the
        Returns:
        - player (Player): the player with the highest score
        """
        max_player = None
        for key, value in score_player.items():
            if max_player is None or score_player[max_player] < value:
                max_player = key
        return max_player

    def end_game(self, player: Player) -> bool:
        """
        Check if it's the end of the game
        Args:
        - player (Player): the player to test
        Returns:
        - player (Player): the player with the highest score
        """
        return len(self.game_map.get_houses_from_player(player)) == 15

    def start(self):
        """
        Method to start the game
        """
        self.initialize_shop()
        self.define_bonus_token_province()
        started = True
        while started:
            for p in self.game_players:
                self.choose_card(p)
                if self.empty_game_shop_available() and len(self.game_shop) == 0:
                    started = False
                if self.end_game(p):
                    started = False
            print("Next Turn")
        score_player = {}
        for p in self.game_players:
            score_player[p] = calculate_score_for_player(player=p, game=self.game_map)
        winner: Player = self.define_winner(score_player)
        print("The winner is : " + winner.player_color)

    def remove_card(self, card: Card):
        """
        Remove the card in param of the game_shop_available
        Args:
        - card (Card): The card to remove
        """
        for display_area, card_shop in self.game_shop_available.items():
            if card == card_shop:
                self.game_shop_available[display_area] = None
                self.replace_card()
