from typing import List
from .good import Good
from .CARDS.card import Card
from .COLONISTS.colonist_pawn import ColonistPawn
from player import Player  # Import the Player class


class IA(Player):  # Inherit from the Player class

    ia_name: str

    def __init__(self,
                 p_player_wallet: int,
                 p_player_color: str,
                 p_player_score: int,
                 p_player_goods: List[Good],
                 p_player_played_cards: List[Card],
                 p_player_playable_cards: List[Card],
                 p_player_colonists_board: List[ColonistPawn],
                 p_player_colonists_inventory: List[ColonistPawn]):
        super().__init__(p_player_wallet, p_player_color, p_player_score,
                         p_player_goods, p_player_played_cards, p_player_playable_cards,
                         p_player_colonists_board, p_player_colonists_inventory)
        self.ia_name = "ia " + p_player_color
