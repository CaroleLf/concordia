from CONCORDIA.METIER.BOARD.city import City
from CONCORDIA.METIER.BOARD.house import House
from CONCORDIA.METIER.CARDS.colonist import Colonist
from CONCORDIA.METIER.LINES.line import Line
from CONCORDIA.METIER.game import Game
from CONCORDIA.METIER.player import Player
from .card import Card
from typing import List

from ..COLONISTS.colonist_pawn import ColonistPawn


class Architect(Card):

    def card_action(self, player: Player, game: Game) -> bool:
        """
        Allow to perform the action of the card

        Args:
            player: the player who use the card
            game: the current game
        """
        max_moves = len(player.player_colonists_board)

        while max_moves > 0:
            print(f"Maximum number of movements : {max_moves}")
            for i, colonist in enumerate(player.player_colonists_board):
                line_colonist_movements = self.get_all_possible_movement_for_one_colonist(colonist, game)

                print(f"Colon {i + 1}:")
                print(f"    Colonist Type: {colonist.colonist_type}")
                print("    Possible movements :")
                for j, line in enumerate(line_colonist_movements):
                    print(f"        {j + 1}. De {line.line_city_1.city_name} à {line.line_city_2.city_name}")

            chosen_colonist = None
            while chosen_colonist is None:
                colonist_choice = int(input("Chose a colonist (number) or leave (0): ")) - 1
                if colonist_choice == -1:
                    return False
                if colonist_choice < len(player.player_colonists_board):
                    chosen_colonist = player.player_colonists_board[colonist_choice]
                else:
                    print(f"Invalid number, choose a number between 1 and {len(player.player_colonists_board)}.")

            line_colonist_movements = self.get_all_possible_movement_for_one_colonist(chosen_colonist, game)
            print(f"Possibles movement for the colon {colonist_choice + 1}:")

            for i, line in enumerate(line_colonist_movements):
                print(f"    {i + 1}. De {line.line_city_1.city_name} à {line.line_city_2.city_name}")

            if len(line_colonist_movements) == 0:
                print("There's no line to go.")

            movement_choice = int(input("Chose a movement (number) : ")) - 1
            chosen_movement = line_colonist_movements[movement_choice]

            # Appliquer le mouvement choisi (vous devrez implémenter cette fonction)
            self.apply_movement(chosen_movement, chosen_colonist, player, game)

            max_moves -= 1

            while True:
                purchase_choice = input("Do you want to buy a house at one "
                                        "end of the line ? (y/n) : ").strip().lower()

                if purchase_choice == "y":
                    city_choice = input(f"In which city you want put a house ? "
                                        f"({chosen_movement.line_city_1.city_name} (1) or "
                                        f"{chosen_movement.line_city_2.city_name} (2) | leave (3)) : ").strip()

                    if city_choice == "1":
                        city = chosen_movement.line_city_1
                    elif city_choice == "2":
                        city = chosen_movement.line_city_2
                    elif city_choice == "3":
                        break
                    else:
                        print("Invalid city choice.")
                        continue

                    if city.city_is_capital:
                        print("You can't bough a house in capital.")
                        continue

                    if any(house.house_player == player
                           and house.house_city == city
                           for house in game.game_map.map_coll_houses):
                        print("You already have a house in this city.")
                        continue  # Redemande l'achat de maison

                    end_city = player.purchase_house(city)
                    if end_city is not None:
                        house = House(end_city, player)
                        game.game_map.map_coll_houses.append(house)
                    break  # Sort de la boucle de choix

                else:
                    break
        return True

    def apply_movement(self, chosen_movement: Line, chosen_colonist: Colonist, player: Player, game: Game):
        """
        Allow player to apply his chose movement
        """
        line_city_1 = chosen_movement.line_city_1
        line_city_2 = chosen_movement.line_city_2

        city_base = None
        for prov in game.game_map.map_coll_provinces:
            for city in prov.province_coll_citys:
                if chosen_colonist in city.city_colonists:
                    city_base = city

        if city_base is None:
            for line in game.game_map.map_coll_line:
                if line.line_colonist == chosen_colonist:
                    line.line_colonist = None
        else:
            city_base.city_colonists.remove(chosen_colonist)

        chosen_movement.line_colonist = chosen_colonist

        print(f"The colon has been move between {line_city_1.city_name} and {line_city_2.city_name}.")

    def get_all_possible_movement_for_one_colonist(self,
                                                   colonist: Colonist,
                                                   game: Game):
        """
        Allow to get all the movement possibilities of one colonist

        Args:
            colonist: the colonist to move
            game: the current game

        return List[Line]
        """
        line_colonist_movements = []
        all_cities = []

        for prov in game.game_map.map_coll_provinces:
            for city in prov.province_coll_citys:
                if colonist in city.city_colonists:
                    all_cities.append(city)

        if colonist in game.game_map.map_capital.city_colonists:
            all_cities.append(game.game_map.map_capital)

        line_colonist_movements = self.get_all_lines_movements(all_cities,
                                                               colonist, game)

        if len(line_colonist_movements) == 0:
            for line in game.game_map.map_coll_line:
                if colonist == line.line_colonist:
                    line_colonist_movements = self.get_all_lines_movements(
                        [line.line_city_1, line.line_city_2],
                        colonist, game)

        return line_colonist_movements

    def get_all_lines_movements(self,
                                citys: List[City],
                                colonist: ColonistPawn,
                                game: Game):
        """
        Allow to get all the movement possibilities from one line

        Args:
            citys: a list with all the cities of the game
            colonist: the colonist to move
            game: the current game

        return List[Line]
        """
        line_colonist_movements = []
        for city in citys:
            for line in game.game_map.map_coll_line:
                if (line.line_city_1.city_name.lower() == city.city_name.lower()
                    or line.line_city_2.city_name.lower() == city.city_name.lower()) \
                        and line.line_way.way_name.lower() == colonist.colonist_type.lower() \
                        and line.line_colonist != colonist:
                    if line not in line_colonist_movements:
                        line_colonist_movements.append(line)
        return line_colonist_movements
