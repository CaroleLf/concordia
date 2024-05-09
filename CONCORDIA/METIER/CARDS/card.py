from typing import List
from abc import ABC, abstractmethod
from ..good import Good
from ..god import God
from ..numeral import Numeral


class Card(ABC):
    card_name: str
    card_description: str
    card_example: str
    card_god: God
    card_buy: bool
    card_for_sale_deck: List[Numeral]
    card_goods_cost: List[Good]

    def __init__(self,
                 p_card_name: str,
                 p_card_description: str,
                 p_card_example: str,
                 p_card_god: God,
                 p_card_for_sale_deck: List[Numeral],
                 p_card_goods_cost: List[Good],
                 p_card_buy: bool = True) -> None:
        self.card_name = p_card_name
        self.card_description = p_card_description
        self.card_example = p_card_example
        self.card_god = p_card_god
        self.card_for_sale_deck = p_card_for_sale_deck
        self.card_goods_cost = p_card_goods_cost
        self.card_buy = p_card_buy

    @abstractmethod
    def card_action(self) -> None:
        pass
