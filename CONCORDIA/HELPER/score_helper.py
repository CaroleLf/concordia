from typing import List

from CONCORDIA.METIER.BOARD.map import Map
from CONCORDIA.METIER.CARDS.specialist import Specialist
from CONCORDIA.METIER.good import Good
from CONCORDIA.METIER.player import Player


def calculate_score_for_player(player: Player, map: Map) -> int:
    """
    Calculates the score for a given player based on the cards they have played.

    Args:
        player (Player): The player for whom the score is being calculated.
        map (Map): The game map.

    Returns:
        int: The calculated score for the player.
    """
    score = 0
    for card in player.player_played_cards:
        match card.card_god.god_name:
            case "CONCORDIA":
                score += 7
            case "VESTA":
                score += calculate_score_for_vesta(player)
            case "JVPITER":
                score += calculate_score_for_jupiter(player, map)
            case "SATVRNVS":
                score += calculate_score_for_saturne(player, map)
            case "MERCVRIVS":
                score += calculate_score_for_mercurius(player, map)
            case "MARS":
                score += calculate_score_for_mars(player)
            case "MINERVA":
                if isinstance(card, Specialist):
                    score += calculate_score_for_minerva(player, map, card.speciality)
    return score


def calculate_score_for_vesta(player: Player) -> int:
    """
    Calculates the score for a player with Vesta.

    The score is calculated by adding up the price of all the goods in the player's inventory,
    removing the goods from the inventory, and then dividing the total price by 10.

    Args:
        player (Player): The player object for which to calculate the score.

    Returns:
        int: The calculated score for the player.
    """
    for good in player.player_goods:
        player.player_wallet += good.good_price
        player.player_goods.remove(good)
    return player.player_wallet // 10


def calculate_score_for_jupiter(player: Player, map: Map) -> int:
    """
    Calculates the score for a player with Jupiter based on the number of houses they own that don't produce
    bricks.

    Args:
        player (Player): The player whose score is being calculated.
        map (Map): The game map.

    Returns:
        int: The player's score with Jupiter.
    """
    houses = filter(lambda house: house.house_city.city_good.good_name != "brick" and house.house_player == player,
                    map.map_coll_houses)
    return len(list(houses))


def calculate_score_for_saturne(player: Player, map: Map) -> int:
    """
    Calculates the score for a player with Saturne based on the number of provinces containing their houses.

    Args:
        player (Player): The player for whom the score is being calculated.
        map (Map): The game map.

    Returns:
        int: The score for the player.
    """
    player_city_names = {house.house_city.city_name for house in map.map_coll_houses if house.house_player == player}
    provinces_containing_houses = [province for province in map.map_coll_provinces
                                   if any(city.city_name in player_city_names for city in province.province_coll_citys)]
    return len(provinces_containing_houses)


def calculate_score_for_mercurius(player: Player, map: Map) -> int:
    """
    Calculates the score for the player based on the number of unique goods they have in their houses.

    Args:
    - player (Player): The player for whom the score is being calculated.
    - map (Map): The map object containing all the houses and cities.

    Returns:
    - int: The score for the player.
    """
    player_houses = filter(lambda house: house.house_player == player, map.map_coll_houses)
    player_houses = list(player_houses)
    goods: List[Good] = []
    for house in player_houses:
        if house.house_city.city_good not in goods:
            goods.append(house.house_city.city_good)
    return len(goods) * 2


def calculate_score_for_mars(player: Player) -> int:
    """
    Calculates the score for a player based on the number of colonists they have on Board.

    Args:
    - player (Player): The player object for whom the score is being calculated.

    Returns:
    - int: The score calculated based on the number of colonists the player have on the Board.
    """
    return min(len(player.player_colonists_board) * 2, 10)


def calculate_score_for_minerva(player: Player, map: Map, speciality: Good) -> int:
    """
    Calculates the score for a player based on the number of houses they own that produce a specific good.

    Args:
        player (Player): The player for whom the score is being calculated.
        map (Map): The game map.
        speciality (Good): The good for which the player's houses are producing.

    Returns:
        int: The score for the player.
    """
    player_houses = filter(lambda house: house.house_player == player
                           and house.house_city.city_good.good_name == speciality.good_name,
                           map.map_coll_houses)
    return len(list(player_houses)) * speciality.good_price
