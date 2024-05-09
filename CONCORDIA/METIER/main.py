import copy
from typing import List
from CONCORDIA.METIER.BOARD.map import Map
from CONCORDIA.METIER.CARDS.card import Card
from CONCORDIA.METIER.LINES.way import Way
from CONCORDIA.METIER.game import Game
from CONCORDIA.DAL.model_fill import fill_cards, fill_gods, fill_numerals, fill_goods, fill_map, fill_way, \
    fill_display_area, fill_city_token
from CONCORDIA.DAL.database_data import get_concordia_setup_player, get_concordia_map, \
    get_concordia_color_player
from CONCORDIA.METIER.COLONISTS.colonist_pawn import ColonistPawn
from CONCORDIA.METIER.good import Good
from CONCORDIA.METIER.numeral import Numeral
from CONCORDIA.METIER.player import Player
import random
from CONCORDIA.METIER.BOARD.house import House
from collections.abc import Mapping


def choose_map(ways: List[Way], numerals: List[Numeral]) -> list[Map | int]:
    """
    Methods to choose a map
    Args:
            ways: List of Way
            numerals: List of Numeral
    Returns: the map choosen

    """
    maps = get_concordia_map()
    invalid_map = True
    invalide_number = True
    number_players = None
    map_id = None
    for i, map_data in enumerate(maps, start=1):
        min_player = int(map_data['MAP_MIN_N_PLAYERS'])
        max_player = int(map_data['MAP_MAX_N_PLAYERS'])
        print(f"{i}. {map_data['MAP_NAME']}")
        print(f"Minimum players: {min_player}")
        print(f"Maximum players: {max_player}")

    while invalid_map:
        map_input = input("Which map would you like to use? Enter the number: ")
        try:
            map_id = int(map_input) - 1
            if 0 <= map_id <= len(maps):
                invalid_map = False
            else:
                print("Invalid map number. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    while invalide_number:
        max_player_selected: int = int(maps[map_id]['MAP_MAX_N_PLAYERS'])
        min_player_selected: int = int(maps[map_id]['MAP_MIN_N_PLAYERS'])

        number_player_str = input("How many players will play? " + str(min_player_selected) + " - "
                                  + str(max_player_selected) + " ")
        try:
            number_players = int(number_player_str)
            if min_player_selected <= number_players <= max_player_selected:
                invalide_number = False
            else:
                print("Invalid number of players. Please enter a number between "
                      + str(min_player_selected) +
                      " and " + str(max_player_selected))
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    return [fill_map(map_id=map_id, ways=ways, numerals=numerals), number_players]


def add_colonists_to_initial(initial_colon: List[ColonistPawn], colonist_type: str, color: str, nb_turn: int):
    for i in range(nb_turn):
        col = ColonistPawn(p_colonist_color=color, p_colonist_type=colonist_type)
        initial_colon.append(col)


def propose_color_to_player() -> [str, List[str]]:
    colors = get_concordia_color_player()
    print("Available colors: ", ", ".join(colors))
    chosen_color = input("Enter the color you want: ").lower()  # Convert input to title case
    if chosen_color in colors:
        return chosen_color, colors
    else:
        print("Invalid choice. Please choose a color from the available options.")
    propose_color_to_player()


def initialize_player(number_player: int, colon: List[str],
                      default_goods_player: List[Good],
                      default_card_player: List[Card], cards: List[Card], map: Map) -> List[Player] | House:
    """
        Method to initialize all the players of the game with their attributes
        Args:
            number_player: number of player for the game
            colon: data of the colon present in the database
            default_card_player: set of cards at the start of the party for each player
            default_goods_player: set of goods at the start of the party for each player
        Returns: Map[str, List[Card]] List of player.

        """
    random_color, colors = propose_color_to_player()
    players = []
    initial_sestertii: int = 5
    for j in range(number_player):
        initial_colon = []
        board_colon = []

        for c in colon:
            way: str = c["SETUP_P_COLON_WAY"]
            number_board: int = int(c["SETUP_P_COLON_N_COLONISTS_CAP"])
            number_total: int = int(c["SETUP_P_COLON_N_COLONISTS"])
            number_inventory = (number_total - number_board)
            if number_total > 0:
                if number_inventory > 0:
                    add_colonists_to_initial(initial_colon,
                                             way,
                                             random_color,
                                             number_inventory)
                    for number_colon_map in range(number_board + 1):
                        c = ColonistPawn(p_colonist_color=random_color, p_colonist_type=way)
                map.map_capital.city_colonists.append(c)
                board_colon.append(c)
        if number_player - 1 == j:
            new_default = default_card_player.copy()
            for card in cards:
                if card.card_name == "PRÆFECTVS MAGNVS":
                    new_default.append(card)
                    p = Player(p_player_wallet=initial_sestertii,
                               p_player_color=random_color,
                               p_player_score=0,
                               p_player_goods=default_goods_player.copy(),
                               p_player_played_cards=[],
                               p_player_playable_cards=new_default,
                               p_player_colonists_board=board_colon,
                               p_player_colonists_inventory=initial_colon)
        else:
            p = Player(p_player_wallet=initial_sestertii,
                       p_player_color=random_color,
                       p_player_score=0,
                       p_player_goods=default_goods_player.copy(),
                       p_player_played_cards=[],
                       p_player_playable_cards=default_card_player.copy(),
                       p_player_colonists_board=board_colon,
                       p_player_colonists_inventory=initial_colon)
        players.append(p)
        colors.remove(random_color)
        initial_sestertii += 1
        if colors:
            random_color = random.choice(colors)
        else:
            random_color = None
    return players


def create_shop(cards: List[Card]) -> Mapping[str, List[Card]]:
    """
    Method that create the shop they are added to the shop according to their associated Roman numbers.
    Args:
        cards: List[Card] all the cart in the database
    Returns: Map[str, List[Card]] Map where roman numbers are the key and their corresponding cards in value.
    """
    shop = {}
    for c in cards:
        if c.card_for_sale_deck:
            for num in c.card_for_sale_deck:
                if num.numeral_roman not in shop.keys():
                    shop[num.numeral_roman] = []
                card_copy = c
                shop[num.numeral_roman].append(card_copy)
    return shop


class Main:
    if __name__ == "__main__":

        # Get data
        ways = fill_way()
        numerals = fill_numerals()
        gods = fill_gods()
        goods = fill_goods()
        cards = fill_cards(gods, goods, numerals)
        display_area = fill_display_area(goods)

        # Cards and goods at the start of the game
        default_card_player = []
        default_goods_player = []
        card_shop = create_shop(cards)
        # Choose the number of player
        setup = get_concordia_setup_player()
        colon = setup["SETUP_P_COLONIST"]
        goods_player = setup["SETUP_P_GOOD"]
        card_player = setup["SETUP_P_CARD"]

        # Recup all the setup card and good for the player
        for good in goods_player:
            for g in goods:
                if good['SETUP_P_GOOD_GOOD'] == g.good_name:
                    if g.good_name == "food":
                        food_1 = g
                        food_2 = g
                        default_goods_player.append(g)
                        default_goods_player.append(g)
                    else:
                        go = g
                        default_goods_player.append(g)
        for card in card_player:
            for c in cards:
                if c.card_name == card['SETUP_P_CARD_CARD']:
                    c.card_buy = False
                    if c.card_name == "PREFECT":
                        for _ in range(2):
                            new_card_instance = copy.deepcopy(c)
                            default_card_player.append(new_card_instance)
                    else:
                        new_card_instance = copy.deepcopy(c)
                        default_card_player.append(new_card_instance)
        map, number_player = choose_map(ways=ways, numerals=numerals)
        players = initialize_player(number_player=number_player,
                                    colon=colon,
                                    default_goods_player=default_goods_player.copy(),
                                    default_card_player=default_card_player,
                                    cards=cards,
                                    map=map)
        map.map_coll_houses = []
        for province in map.map_coll_provinces:
            fill_city_token(province.province_coll_citys)

        g = Game(p_game_map=map,
                 p_game_players=players,
                 p_game_goods=goods,
                 p_game_display_area=display_area,
                 p_game_shop=card_shop)
        g.start()
