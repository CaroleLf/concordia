from .card import Card
from ..BOARD.map import Map
from ..good import Good
from ..player import Player


class Specialist(Card):
    speciality: Good

    def card_action(self, player: Player, map: Map):
        """
        Allow to perform the action of the card

        Args:
            player: the player who use the card
            game: the current game
        """

        test = filter(lambda house: house.house_player == player and house.house_city.city_good == self.speciality,
                      map.map_coll_houses)
        quantity_to_add = len(list(test))
        if quantity_to_add > 0:
            player.add_goods(self.speciality, quantity_to_add)
        return True
