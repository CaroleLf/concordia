from .city import City
from ..player import Player


class House:
    house_city: City
    house_player: Player

    def __init__(self, p_house_city: City, p_house_player: Player) -> None:
        self.house_city = p_house_city
        self.house_player = p_house_player
