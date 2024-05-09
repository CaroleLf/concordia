from typing import List
from ..sdo_point import SDOPoint
from ..good import Good
from ..COLONISTS.colonist_pawn import ColonistPawn


class City:
    city_name: str
    city_roman_char: str
    city_is_capital: bool
    city_coordinates: SDOPoint
    city_good: Good
    city_colonists: List[ColonistPawn]

    def __init__(self,
                 p_city_name: str,
                 p_city_roman_char: str,
                 p_city_is_capital: bool,
                 p_city_coordinates: SDOPoint,
                 p_city_good: Good,
                 p_city_colonists: List[ColonistPawn]) -> None:

        self.city_name = p_city_name
        self.city_roman_char = p_city_roman_char
        self.city_is_capital = p_city_is_capital
        self.city_coordinates = p_city_coordinates
        self.city_good = p_city_good
        self.city_colonists = p_city_colonists
