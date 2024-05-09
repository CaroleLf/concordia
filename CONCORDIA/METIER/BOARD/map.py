from typing import List
from .city import City
from .house import House
from .province import Province
from ..player import Player
from ..sdo_point import SDOPoint
from ..LINES.line import Line


class Map:
    map_name: str
    map_min_player: int
    map_max_player: int
    map_capital: City
    map_coll_provinces: List[Province]
    map_coordinates: SDOPoint
    map_coll_line: List[Line]
    map_coll_houses: List[House]

    def __init__(self,
                 p_map_name: str,
                 p_map_min_player: int,
                 p_map_max_player: int,
                 p_map_capital: City,
                 p_map_coll_provinces: List[Province],
                 p_map_max_coordinates: SDOPoint,
                 p_map_coll_line: List[Line]) -> None:
        self.map_name = p_map_name
        self.map_min_player = int(p_map_min_player)
        self.map_max_player = int(p_map_max_player)
        self.map_capital = p_map_capital
        self.map_coll_provinces = p_map_coll_provinces
        self.map_coordinates = p_map_max_coordinates
        self.map_coll_line = p_map_coll_line
        self.map_coll_houses = []

    def get_all_city(self) -> List[City]:
        """
        Allow to get all the city of the map

        return List[City]
        """

        all_city = []
        for province in self.map_coll_provinces:
            for city in province.province_coll_citys:
                all_city.append(city)
        return all_city

    def add_house(self, city: City, player: Player) -> None:
        """
        Allow to add house on a target city

        Args:
            city: the target city
            player: the player who want to add a city
        """

        self.map_coll_houses.append(House(city, player))

    def get_houses_from_city(self, city: City) -> List[House]:
        """
        Allow to get all house from a target city

        Args:
            city: the target city

        return List[House]
        """

        houses = []
        for house in self.map_coll_houses:
            if house.house_city == city:
                houses.append(house)
        return houses

    def get_houses_from_player(self, player: Player) -> List[House]:
        """
        Allow to get all house from a target player

        Args:
            player: the target player

        return List[House]
        """

        houses = []
        for house in self.map_coll_houses:
            if house.house_player == player:
                houses.append(house)
        return houses

    def get_province_by_name(self, province_name: str) -> Province | None:
        lowercase_input = province_name.lower()

        for province in self.map_coll_provinces:
            if province.province_name.lower() == lowercase_input:
                return province
        print("This province doesn't exist, please retry.")
        return None
