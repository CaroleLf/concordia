from .card import Card
from ..game import Game
from ..player import Player


class Senator(Card):

    def card_action(self, game: Game, player: Player) -> bool:
        """
        Allow to perform the action of the card

        Args:
            game: the current game
            buyable: the cards list with emplacements
            player: the player who use the card
        """
        print("Buyable Cards:")
        all_cards = list(game.game_shop_available.values())
        for i, card in enumerate(all_cards):
            print(f"Card {i + 1}:")
            print(f"Name: {card.card_name}")
            print(f"Description: {card.card_description}")
            print("Goods Cost:")
            for good in card.card_goods_cost:
                print(f"  - {good.good_name}")
            print("-" * 30)

        while True:
            try:
                chosen_card_number = int(input("Which card (enter card number) would you like to buy (0 to exit)? "))
                if chosen_card_number == 0:
                    return False
                elif 1 <= chosen_card_number <= len(all_cards):
                    chosen_card_number -= 1
                    break
                else:
                    print("Invalid card number. Please enter a valid card number.")
            except ValueError:
                print("Invalid input. Please enter a valid card number.")

        if self.buy_card(player, game, all_cards, chosen_card_number):
            game.replace_card()
            return True
        return False

    def buy_card(self, player: Player,
                 game: Game,
                 choosed_card_number: int) -> bool:
        """
        Allow player to buy the card he chooses
        """
        buyable = list(game.game_shop_available.values())
        if not buyable:
            print("No buyable cards available.")
            return False

        if choosed_card_number < 0 or choosed_card_number > len(buyable):
            print("Invalid card number. Please choose a valid card number.")
            return False

        choosed_card_obj = buyable.pop(choosed_card_number - 1)

        goods_to_remove = [good.good_name for good in choosed_card_obj.card_goods_cost]
        enough_goods = True
        logic_executed = False

        for good in goods_to_remove:
            if not player.remove_goods(good, 1):
                print(f"You do not have enough {good} to purchase this card.")
                enough_goods = False
                return False

            if enough_goods and not logic_executed:
                for key, value in game.game_shop_available.items():
                    if value == choosed_card_obj:
                        if player.remove_goods(key.display_area_good.good_name, key.display_area_n_goods):
                            game.game_shop_available[key] = None
                        else:
                            print(f"You do not have enough {good} to purchase this card.")
                            enough_goods = False
                            return False
                logic_executed = True

        player.player_playable_cards.append(choosed_card_obj)

        return True
