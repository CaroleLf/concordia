from typing import List
from .city import City
from ..numeral import Numeral
from ..sdo_point import SDOPoint
from ..BOARD.bonus_token import BonusToken


class Province:
    province_name: str
    province_roman_num: Numeral
    bonus_token: BonusToken

    province_coll_citys: List[City]
    province_coordinates: SDOPoint

    def __init__(self,
                 p_province_name: str,
                 p_province_roman_num: Numeral,
                 p_province_coll_citys: List[City],
                 p_province_coordinates: SDOPoint,
                 bonus_token: BonusToken) -> None:
        self.province_name = p_province_name
        self.province_roman_num = p_province_roman_num
        self.province_coll_citys = p_province_coll_citys
        self.province_coordinates = p_province_coordinates
        self.bonus_token = bonus_token
