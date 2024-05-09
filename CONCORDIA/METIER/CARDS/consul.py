from typing import List

from .card import Card
from ..display_area import DisplayArea
from ..game import Game
from ..good import Good
from ..player import Player


class Consul(Card):

    def card_action(self, player: Player, game: Game) -> bool:
        # Display card buyable
        # if ressource and money are enough card are displayed,else card are display in black and white just filter
        choice_made = False
        display_area = game.game_display_area

        while not choice_made:
            for i in range(0, len(display_area)):
                print(f"{i}. {game.game_shop_available.get(display_area[i]).card_name}")
                print(f"{game.game_shop_available.get(display_area[i]).card_description}")
            print(f"{len(display_area)}. Abort")
            index_chosen_card = int(input("Which card would you like to buy ?"))

            if index_chosen_card == len(display_area):
                return False
            else:
                choice_made = self.choose_card(game, player, index_chosen_card)
        return True

    def choose_card(self, game: Game, player: Player, index_chosen_card: int) -> bool:
        """
        display the cost of the chosen card and ask you if you want to purchase it
        :param game: Game
        :param player: Player
        :param index_chosen_card: int
        :return: bool
        """
        chosen_display_area: DisplayArea = game.game_display_area[index_chosen_card]

        necessary_goods_count = self.get_good_counts(game.game_shop_available.get(chosen_display_area).card_goods_cost)

        if self.buyable(player, necessary_goods_count):
            print("It will cost you")
            for good in necessary_goods_count:
                print(f"{good[1]} {good[0]}")

            choice_made = False
            while not choice_made:
                response = int(input("Do you want to continue buy this card ?(Y/N"))
                if response == "Y":
                    self.buy_card(game, player, chosen_display_area)
                    return True
                elif response == "N":
                    return False
                else:
                    print("Invalid input.")
        else:
            print("You don't have enough resources")

    def buy_card(self, game: Game, player: Player, chosen_display_area: DisplayArea) -> None:
        """
        buy a card and put it in the player deck
        :param game: Game
        :param player: Player
        :param chosen_display_area: DisplayArea
        :return: None
        """
        goods = self.get_good_counts(game.game_shop_available.get(chosen_display_area).card_goods_cost)
        for good in goods:
            print(good)
            player.remove_goods(good, goods[good])
        player.player_playable_cards.append(game.game_shop_available.get(chosen_display_area))
        game.game_shop_available[chosen_display_area] = None

    def buyable(self, player: Player, necessary_goods_count: dict) -> bool:
        """
        return if a card is buyable
        :param player: Player
        :param necessary_goods_count: dict
        :return: bool
        """
        for ngood in necessary_goods_count:
            if necessary_goods_count[ngood] > player.get_good_counts().get(ngood):
                return False
        return True

    def get_good_counts(self, goods: List[Good]) -> dict:
        """
        return a dictionary of resources and their quantity
        :param goods: List[Good]
        :return: dict
        """
        good_counts = {}
        for good in goods:
            if good.good_name.lower() not in good_counts:
                good_counts[good.good_name.lower()] = 1
            else:
                good_counts[good.good_name.lower()] += 1
        return good_counts
