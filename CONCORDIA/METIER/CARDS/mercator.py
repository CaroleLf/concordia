from .card import Card
from ..player import Player
from ..game import Game
from ..good import Good


class Mercator(Card):

    def card_action(self, player: Player, game: Game) -> bool:
        """
        Allow to perform the action of the card

        Args:
            player: the player who use the card
            game: the current game
        """

        if self.card_buy:
            player.player_wallet += 5
        else:
            player.player_wallet += 3

        print(f"You have {player.player_wallet} sesterii in your wallet")
        correct_choice = False
        while not correct_choice:
            trade_choice = input("Do you want to exchange goods? (Y/N): ").lower()
            if trade_choice.lower() == "y":
                self.trade_goods(player, game)
                return True
            elif trade_choice.lower() == "n":
                return False
            else:
                print("Invalid input.")

    def trade_goods(self, player: Player, game: Game) -> None:
        """
        Allow to show trade menu

        Args:
            player: the player who want to trade some goods
            game: the current game
        """

        print("Here are your goods:")
        for good_name, count in player.get_good_counts().items():
            print(f"- {good_name} x{count}")

        correct_choice = False
        while not correct_choice:
            input_msg = ("Do you want to sell (s) or buy (b) goods "
                         "or leave market (l) ?")
            trade_option = input(input_msg).lower()

            if trade_option == "s":
                self.sell_goods(player)
                correct_choice = True
            elif trade_option == "b":
                if player.player_wallet >= 3:
                    self.buy_goods(player, game)
                    correct_choice = True
                else:
                    print("You don't have enough sesterii to buy any good.")
                    correct_choice = False
            elif trade_option == "l":
                print("You left the exchange.")
                correct_choice = False

    def sell(self, player: Player, selected_good: Good, quantity_to_sell: int) -> bool:
        """
        Allow to ask to sell some goods

        Args:
            player: the player who want to trade some goods
            selected_good: the good to sell
            quantity_to_sell: the quantity of the good to sell
        """

        if player.remove_goods(selected_good.good_name, quantity_to_sell):
            total_earnings = selected_good.good_price * quantity_to_sell
            player.player_wallet += total_earnings

            print(
                f"You sold {quantity_to_sell} {selected_good.good_name}"
                f"for {total_earnings} sester.")
            return True
        else:
            print("Invalid quantity."
                  "Please enter a valid quantity to sell.")
            return False

    def sell_goods(self, player: Player) -> None:
        """
        Allow to sell goods for money

        Args:
            player: the player who want to trade some goods
        """

        good_name = input(
            "What good do you want to sell? (enter the good's name)").lower()

        if good_name in player.get_good_names():
            selected_good = player.get_good_by_name(good_name)

            max_quantity = player.get_good_count(good_name)

            correct_choice = False
            while not correct_choice:
                input_msg = (f"How many {selected_good.good_name}"
                             f"do you want to sell? "
                             f"(maximum {max_quantity})")
                quantity_to_sell = int(input(input_msg))

                correct_choice = self.sell(player, selected_good, quantity_to_sell)
        else:
            print("You don't have that type of good.")

    def buy(self, player: Player, selected_good: Good, quantity_to_buy: int) -> bool:
        """
        Allow to ask to buy some goods

        Args:
            player: the player who want to buy some goods
            selected_good: the good to sell
            quantity_to_sell: the quantity of the good to buy
        """

        if player.player_wallet >= selected_good.good_price * quantity_to_buy:

            wallet = player.player_wallet
            max_quantity = min(12 - len(player.player_goods) - len(player.player_colonists_inventory),
                               wallet // selected_good.good_price)

            if quantity_to_buy <= max_quantity:
                total_price = selected_good.good_price * quantity_to_buy
                inventory_filled = len(player.player_goods)
                inventory_filled += len(player.player_colonists_inventory)
                inventory_filled += quantity_to_buy
                if inventory_filled <= 12:
                    player.player_goods.extend(
                        [selected_good] * quantity_to_buy)
                    player.player_wallet -= total_price
                    print(f"""You bought {quantity_to_buy}
                        {selected_good.good_name}
                        for {total_price} sester.""")
                else:
                    print("Your inventory is full."
                          "Sell some goods before buying more.")
                    return True
            else:
                print("Invalid quantity."
                      "Please enter a valid quantity to buy.")
                return False
        else:
            print("You don't have enough money"
                  "to buy this quantity of goods.")
            return True

    def buy_goods(self, player: Player, game: Game) -> None:
        """
        Allow to buy some goods

        Args:
            player: the player who want to trade some goods
            game: the current game
        """

        print(f"You have {player.player_wallet} sesterii")
        print("Available goods to buy:")
        for i, good in enumerate(game.game_goods):
            print(f"{i}. {good.good_name} - Price: {good.good_price}")

        correct_choice = False
        while not correct_choice:
            good_index = int(
                input("What good do you want to buy? (enter number)"))
            selected_good = game.game_goods[good_index]

            quantity_to_buy = int(
                input(f"How many {selected_good.good_name} do you want to buy?"))

            correct_choice = self.buy(player, selected_good, quantity_to_buy)
