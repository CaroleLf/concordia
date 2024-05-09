from typing import List
from .card import Card
from ..BOARD.province import Province
from ..player import Player
from ..BOARD.map import Map
from ..BOARD.bonus_token import BonusToken


class Prefect(Card):

    def card_action(self, player: Player, map: Map) -> bool:
        chosen_province: Province = None
        while chosen_province is None:
            for province in map.map_coll_provinces:
                print(province.province_name)
            chosen_province_str = input("Which province do you want to collect goods from ? ")
            correct_choice = False
            while not correct_choice:
                chosen_province = map.get_province_by_name(chosen_province_str.lower())
                if chosen_province is not None:
                    correct_choice = True
                else:
                    print("Invalid input.")

        # verification bonus token returned
        if chosen_province.bonus_token.is_returned:
            correct_choice = False
            while not correct_choice:
                answer = input("Do you want to collect bonus cash (y n)?")
                if answer.lower() == "y":
                    self.collect_bonus_cash(map.map_coll_provinces, player)
                    print(player.player_wallet)
                    correct_choice = True
                elif answer.lower() == "n":
                    self.collect_goods(player, map, chosen_province)
                    correct_choice = True
                    # bonus token not returned
        else:
            self.collect_bonus_token(chosen_province.bonus_token, player)
            self.collect_goods(player, map, chosen_province)
        return True

    def collect_goods(self, player: Player, map: Map, province: Province) -> None:
        """
        Allow to collect the goods of the cities of the province

        Args:
            province : the province where we collect the goods
        """
        houses = map.get_houses_from_player(player)
        for house in houses:
            if house.house_city in province.province_coll_citys:
                player.add_good(house.house_city.city_good)

    def collect_bonus_token(self, bonus_token: BonusToken, player: Player) -> None:
        """
        Allow to collect the good of the bonus token

        Args:
            bonus_token : the bonus token where we collect the good
            player : the player who collect the bonus token
        """

        player.add_good(bonus_token.target_good)
        print(f"You receive {bonus_token.target_good.good_name} from the bonus token")

    def collect_bonus_cash(self, provinces: List[Province], player: Player) -> None:
        """
        Allow to collect all the cash of the returned bonus token

        Args:
            provinces : the list of the province
        """

        total_cash: int = 0

        for province in provinces:
            bonus_token = province.bonus_token
            if bonus_token.is_returned:
                total_cash += bonus_token.bonus_sesters

        player.player_wallet += total_cash
        print(f"You receive {total_cash} sesteriis")
