from .card import Card
from ..player import Player
from ..game import Game


class Diplomat(Card):

    def play_last_card_of_player(self, player: Player, target_player: Player, game: Game) -> bool:
        """
        Allow player to copy the last played card of the chosen player

        Args:
            player: the player who want to copy a card
            target_player: the player who has his card copied
        """

        chosen_card = target_player.get_last_played_card()
        if chosen_card:
            if chosen_card.card_name.lower() != "diplomat":
                player.player_playable_cards.append(chosen_card)
                print(f"You copied {chosen_card.card_name} from "
                      f"{target_player.player_color} to {player.player_color}.")
                game.define_parameter_card(player.player_playable_cards[len(player.player_playable_cards) - 1], player)
            else:
                print("You can't copy diplomat")
        else:
            print(f"{target_player.player_color} doesn't have a card played.")
            return False

    def card_action(self, player: Player, game: Game):
        """
        Allow to perform the action of the card

        Args:
            player: the player who use the card
            game: the current game
        """
        count = 0
        last_played_card = None
        for other_player in game.game_players:
            if other_player != player:
                last_played_card = other_player.get_last_played_card()
                if last_played_card and last_played_card.card_name.lower() != "diplomat":
                    print(f"- {other_player.player_color}:"
                          f"{last_played_card.card_name}")
                    count += 1
        if count == 0:
            print("There is no cards played by any player or they are Diplomat Card.")
            return False
        else:
            chosen_player = None
            while chosen_player is None:
                chosen_player_color = input(
                    "Choose a player to copy a card from: ")
                chosen_player = game.find_player_by_color(
                    chosen_player_color.lower(), game.game_players)
                if chosen_player is None:
                    print(f"There is no player {chosen_player_color}."
                          f" Please choose a valid player.")

            self.play_last_card_of_player(player, chosen_player, game)
