from .way import Way
from ..BOARD.city import City
from ..COLONISTS.colonist_pawn import ColonistPawn


class Line:
    line_city_1: City
    line_city_2: City
    line_colonist: ColonistPawn
    line_way: Way

    def __init__(self,
                 p_line_city_1: City,
                 p_line_city_2: City,
                 p_line_colonist: ColonistPawn,
                 p_line_way: Way):
        self.line_city_1 = p_line_city_1
        self.line_city_2 = p_line_city_2
        self.line_colonist = p_line_colonist
        self.line_way = p_line_way
