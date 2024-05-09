from typing import List
from CONCORDIA.METIER.BOARD.city import City
from .good import Good
from .CARDS.card import Card
from .COLONISTS.colonist_pawn import ColonistPawn


class Player:
    player_wallet: int
    player_color: str
    player_score: int
    player_inventory: int = 12
    player_goods: List[Good]
    player_played_cards: List[Card]
    player_playable_cards: List[Card]
    player_colonists_board: List[ColonistPawn]
    player_colonists_inventory: List[ColonistPawn]

    def __init__(self,
                 p_player_wallet: int,
                 p_player_color: str,
                 p_player_score: int,
                 p_player_goods: List[Good],
                 p_player_played_cards: List[Card],
                 p_player_playable_cards: List[Card],
                 p_player_colonists_board: List[ColonistPawn],
                 p_player_colonists_inventory: List[ColonistPawn]):
        self.player_wallet = p_player_wallet
        self.player_color = p_player_color
        self.player_score = p_player_score
        self.player_goods = p_player_goods
        self.player_played_cards = p_player_played_cards
        self.player_playable_cards = p_player_playable_cards
        self.player_colonists_board = p_player_colonists_board
        self.player_colonists_inventory = p_player_colonists_inventory

    def get_good_counts(self) -> dict:
        """
        Allow to get the list of goods and the number owned

        return dict
        """

        good_counts = {}
        for good in self.player_goods:
            if good.good_name.lower() not in good_counts:
                good_counts[good.good_name.lower()] = 1
            else:
                good_counts[good.good_name.lower()] += 1
        return good_counts

    def get_good_names(self) -> List[str]:
        """
        Allow to get the name of the possesses goods

        return List[str]
        """

        return [good.good_name.lower() for good in self.player_goods]

    def get_good_by_name(self, good_name: str) -> Good | None:
        """
        Allow to get a good with his name

        Args:
            good_name : The name of the good to get

        return Good
        """

        for good in self.player_goods:
            if good.good_name.lower() == good_name.lower():
                return good
        return None

    def get_good_count(self, good_name: str) -> int:
        """
        Allow to get the number of one good

        Args:
            good_name : the good that we want to know the number owned

        return int
        """

        return self.get_good_counts().get(good_name, 0)

    def remove_goods(self, good_name: str, quantity: int) -> bool:
        """
        Allow to remove a good from the list

        Args:
            good_name : the good to remove
            quantity : the quantity of good to remove

        return bool
        """

        max_quantity = self.get_good_count(good_name)
        if quantity <= max_quantity:
            for good in self.player_goods:
                if good.good_name.lower() == good_name.lower() and quantity > 0:
                    quantity -= 1
                    self.player_goods.remove(good)
            return True
        else:
            return False

    def add_goods(self, good: Good, quantity: int) -> None:
        """
        Allow to add some goods to the list

        Args:
            good: the good to add
            quantity: the quantity of the good to add
        """

        for _ in range(quantity):
            self.add_good(good)

    def add_good(self, good: Good) -> None:
        """
        Allow to add a good to the list

        Args:
            good: the good to add
        """

        size_inventory: int = len(self.player_goods) + len(self.player_colonists_inventory)
        if size_inventory < self.player_inventory:
            self.player_goods.append(good)

    def get_last_played_card_by_name(self, card_name) -> Card | None:
        """
        Allow to get the last played card by name

        Args:
            card_name: the name of the card to get

        return Card
        """

        for card in reversed(self.player_played_cards):
            if card.card_name.lower() == card_name.lower():
                return card
        return None

    def get_last_played_card(self) -> Card | None:
        """
        Allow to know the lasted card played by the player
        """
        if self.player_played_cards:
            return self.player_played_cards[-1]
        return None

    def get_count_colonist_inventory(self) -> dict:
        colonist_counts = {}
        for colonist in self.player_colonists_inventory:
            if colonist.colonist_type.lower() not in colonist_counts:
                colonist_counts[colonist.colonist_type.lower()] = 1
            else:
                colonist_counts[colonist.colonist_type.lower()] += 1
        return colonist_counts

    def get_count_colonist_inventory_by_type(self, colonist_type: str) -> int:
        return self.get_count_colonist_inventory().get(colonist_type, 0)

    def get_colonist_inventory_by_type(self, colonist_type: str) -> ColonistPawn | None:
        for colonist in self.player_colonists_inventory:
            if colonist.colonist_type.lower() == colonist_type.lower():
                return colonist
        return None

    def add_colonist(self, colonist: ColonistPawn) -> None:
        """
        Allow to add a colonist to the invenory of the player

        Args:
            colonist: the colonist to add
        """
        self.player_colonists_inventory.append(colonist)

    def purchase_house(self, city: City):
        """
        Allow player to purchase a house
        """
        cost = 0
        has_materials = False

        if city.city_good.good_name.lower() == "wine":
            cost = 4
            has_materials = self.has_materials(city.city_good.good_name)
        elif city.city_good.good_name.lower() == "tool":
            cost = 3
            has_materials = self.has_materials(city.city_good.good_name)
        elif city.city_good.good_name.lower() == "food":
            cost = 2
            has_materials = self.has_materials(city.city_good.good_name)
        elif city.city_good.good_name.lower() == "brick":
            cost = 1
            has_materials = self.has_materials(city.city_good.good_name)
        elif city.city_good.good_name.lower() == "cloth":
            cost = 5
            has_materials = self.has_materials(city.city_good.good_name)

        if self.player_wallet < cost:
            print("You don't have enough money to buy a house.")
            return None

        if not has_materials:
            print("You don't have enough materials to buy a house.")
            return None

        self.remove_materials(city.city_good.good_name)
        self.player_wallet -= cost

        print("You have successfully purchased a house.")

        return city

    def has_materials(self, city_good_name):
        """
        Allow to know if the player has necessary materials to purchase the house
        """
        if city_good_name.lower() == "brick":
            return self.get_good_count("wheat") >= 1
        else:
            return self.get_good_count("brick") >= 1 and self.get_good_count(city_good_name) >= 1

    def remove_materials(self, city_good_name):
        """
        Allow to remove material after purchase a house
        """
        if city_good_name.lower() == "brick":
            self.remove_goods("wheat", 1)
        else:
            self.remove_goods("brick", 1)
            self.remove_goods(city_good_name, 1)

    def remove_card(self, card):
        """
        Allow to remove card in the deck of the player
        """
        i: int = 0
        remove: bool = False
        while i < len(self.player_playable_cards) - 1 and not remove:
            if card.card_name == self.player_playable_cards[i].card_name:
                self.player_played_cards.append(self.player_playable_cards.pop(i))
                remove = True
            i += 1

    def have_prafectus_magnus(self):
        """
        Method that return a boolean, true if the player has
        the card PRÆFECTVS MAGNVS else false
        """
        for c in self.player_playable_cards:
            if c.card_name == "PRÆFECTVS MAGNVS":
                return True
        return False
