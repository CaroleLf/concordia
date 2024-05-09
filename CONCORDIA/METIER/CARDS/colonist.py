from typing import List
from .card import Card
from ..player import Player
from ..BOARD.house import House

'''
Colonist card
Actions :
    -The player places new colonists
    (inside “Roma” or inside any other
city where the player owns a house)
on the game board, each paid
with 1 food and 1 tool.
    -The player receives 5 sestertii plus
    1 sestertius for each of his/her
colonists on the game board.
'''


class Colonist(Card):

    def card_action(self, player: Player, player_houses: List[House]) -> bool:
        """
        Allow to perform the action of the card

        Args:
            player: the player who use the card
            player_houses: the houses owned by the player
        """
        correct_choice = False
        while not correct_choice:
            player_choice = input('''Do you want to place new colonists?
                  It will cost you 1 food and 1 tool (Y/N): ''').lower()
            if player_choice.lower() == "y":
                self.place_colonists(player, player_houses)
                correct_choice = True
            elif player_choice.lower() == "n":
                self.get_sestertii_from_colonists(player)
                correct_choice = True
            else:
                print("Invalid input")

        return True

    def place_colonists(self, player: Player, player_houses: List[House]) -> None:
        """
        Place colonists in a city
        Remove 1 food and 1 tool and 1 colonist from the player
        :param player: Player
        :param player_houses: List[House]
        :return: None
        """
        if len(player.player_colonists_inventory) == 0:
            print("You don't have any colonists left")
            self.get_sestertii_from_colonists(player)
        elif (player.get_good_count("food") >= 1
              and player.get_good_count("tool") >= 1):
            player.remove_goods("food", 1)
            player.remove_goods("tool", 1)
            if len(player_houses) == 0:
                print("You don't have any houses")
                self.get_sestertii_from_colonists(player)
            else:
                print("Cities where you can place your colonists: ")
                player_houses_city = []
                for house in player_houses:
                    player_houses_city.append(house.house_city.city_name)
                    print(f"- {house.house_city.city_name}")
                correct_choice = False
                while not correct_choice:
                    city_choice = input('''Where do you want
                     to place your colonists?
                     (enter the city's name): ''')
                    print(f"city_choice: {city_choice}")
                    if city_choice in player_houses_city:
                        for house in player_houses:
                            if house.house_city.city_name.lower() == city_choice.lower():
                                house.house_city.city_colonists.append(
                                    player.player_colonists_inventory.pop())
                                print(f"You placed a colonist in {city_choice}")
                                correct_choice = True
                    else:
                        print("Invalid input")
        else:
            print("You don't have enough food or tool")
            self.get_sestertii_from_colonists(player)

    def get_sestertii_from_colonists(self, player: Player) -> None:
        """
        Give the player 5 sestertii + 1 sestertius for each of his/her
        colonists on the game board
        :param player: Player
        :return: None
        """
        added_sestertii = 5
        added_sestertii += player.player_colonists_board.__len__()
        player.player_wallet += added_sestertii
        print(f"You received {added_sestertii} sestertii")
