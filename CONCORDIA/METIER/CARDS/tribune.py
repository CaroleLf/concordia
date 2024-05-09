from CONCORDIA.METIER.player import Player
from CONCORDIA.METIER.BOARD.map import Map
from CONCORDIA.METIER.CARDS.card import Card
from CONCORDIA.METIER.COLONISTS.colonist_pawn import ColonistPawn


class Tribune(Card):

    def card_action(self, player: Player, map: Map) -> bool:
        """
        Allow to perform the action of the card

        Args:
            map: the current map
            player: the player who use the card
            :return: bool
        """

        sesteriis_earn = 0

        if len(player.player_played_cards) > 3:
            sesteriis_earn += len(player.player_played_cards) - 3

        player.player_wallet += sesteriis_earn
        print(f"You receive {sesteriis_earn} sesteriis")

        player.player_playable_cards.extend(player.player_played_cards)
        player.player_played_cards = []
        self.choose_to_buy(player, map)
        return True

    def choose_to_buy(self, player: Player, map: Map) -> None:
        """
        Allow you to choose if you want to buy a colonist

        :param player: Player
        :param map: Map
        :return: None
        """
        if ((player.get_good_count('tool') >= 1
            and player.get_good_count('food') >= 1)
                and (player.get_count_colonist_inventory() != {})):
            action_done = False
            while not action_done:
                quantity_earth_colonist = player.get_count_colonist_inventory_by_type("land")
                quantity_water_colonist = player.get_count_colonist_inventory_by_type("sea")
                input_msg = (f"\nYou have {quantity_earth_colonist} Land colonist"
                             f" and {quantity_water_colonist} Sea colonist in your inventory"
                             "\nDo you want to buy a new colonist ?"
                             "\n(Y/N)")

                response = str(input(input_msg))

                action_done = self.choose_colonist_type(player, map, response)
        else:
            print("You can't place a new colonist.")

    def choose_colonist_type(self, player: Player, map: Map, choice: str) -> bool:
        """
        Choose a value to determine the type of the colonist.
        If you have only one type of colonist, it's automaticly choosen
        :param player: Player
        :param map: Map
        :param choice: str
        :return: bool
        """
        if choice.upper() == "Y":
            choice_done = False
            while not choice_done:
                if len(player.get_count_colonist_inventory()) > 1:
                    input_msg = (
                        "Which type of colonist do you want to place ?"
                        "\n Land"
                        "\n Sea"
                        "\n Cancel"
                        )

                    response = str(input(input_msg))

                    choice_done = self.choose_colonist(player, map, response)
                else:
                    self.buy_colonist(player, map, player.player_colonists_inventory[0])
                    choice_done = True
        elif choice.upper() == "N":
            return True
        else:
            print("invalid input."
                  "\nOnly 'Y' or 'N' are accepted.")
            return False
        return True

    def choose_colonist(self, player: Player, map: Map, choice: str) -> bool:
        """
        Choose a colonist depending on the value of choice.
        Return True if the choice is valid and False, if not.
        :param player: Player
        :param map: Map
        :param choice: int
        :return: bool
        """
        if choice.lower() == "land" or choice.lower() == "sea":
            colonist = player.get_colonist_inventory_by_type(choice.lower())

            self.buy_colonist(player, map, colonist)
            return True
        elif choice.lower == "cancel":
            return True
        else:
            print("Invalid input.")
            return False

    def buy_colonist(self, player: Player, map: Map, colonist: ColonistPawn) -> None:
        """
        Take one food and one tool from the player inventory and place the choosen colonist on Rome
        :param player: Player
        :param map: Map
        :param colonist: ColonistPawn
        :return: None
        """
        if player.get_good_count('tool') >= 1 and player.get_good_count('food') >= 1:
            player.remove_goods('food', 1)
            player.remove_goods('tool', 1)
            player.player_colonists_inventory.remove(colonist)
            player.player_colonists_board.append(colonist)
            map.map_capital.city_colonists.append(colonist)
            print("Your colon has been placed on the capital.")
        else:
            print("You don't have enough resources.")
