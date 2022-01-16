"""Implementation of the card game 'War'"""
import random


class Deck ():
    """Class for deck of cards."""
    nums = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    suits = ["S", "C", "D", "H"]
    deck = []

    def __init__(self):
        """Create deck of 52 cards."""
        for num in self.nums:
            for suit in self.suits:
                self.deck.append((num, suit))

    def shuffle(self):
        """Randomize the deck."""
        random.shuffle(self.deck)

    def deal(self):
        """
        Split the deck in half.

        Returns:
            list of tuples (num, suit), list of tuples (num, suit): two halves of deck.
        """
        half = int(len(self.deck)/2)
        return (self.deck[:half], self.deck[half:])


class Player():
    """Class for players"""
    name = "DEFAULT"
    cards = []

    def __init__(self, name, deck):
        """
        Player gets name and deck of cards.

        Arguments:
            name (string): name of player.
            deck (Deck): deck of cards.
        """
        self.name = name
        self.cards = deck

    def reveal(self, is_war):
        """
        Reveal top card if not war. Reveal three cards if war.

        Arguments:
            is_war (bool): if war or not

        Returns:
            list of tuples (num, suit): if war, three cards.
            tuple (num, suit): if not war, one card.
        """
        if is_war:
            cards = []
            for _ in range(3):
                cards.append(self.cards.pop())
            return cards
        else:
            return self.cards.pop()

    def take(self, active_cards):
        """
        Add cards on board to bottom of deck.

        Arguments:
            active_cards (list of tuples (num, suit)): card on the board
        """
        self.cards = active_cards + self.cards
        active_cards.clear()


class WarGame():
    """Class for War gameplay."""
    deck = []

    def __init__(self, player_name, deck, deck1, deck2):
        """
        Set deck and create two players.

        Arguments:
            player_name (string): Name of player.
            deck (Deck): Deck class.
            deck1 (Deck): Cards for player 1.
            deck2 (Deck): Cards for player 2.
        """
        self.deck = deck
        self.player = Player(player_name, deck1)
        self.hal = Player("HAL", deck2)

    def get_winner(self):
        """ 
        Gets winner of the game (whoever has the most cards).

        Returns:
            string: Winner name.
        """
        return self.player.name if len(self.player.cards) > len(self.hal.cards) else self.hal.name

    def get_value(self, card):
        """
        Gets the value of the card based on its index in the array.

        Arguments:
            card (tuple (num, suit)): card to check value.

        Returns:
            int: index/value of the card.
        """
        return self.deck.nums.index(card[0])

    def enough_cards(self, cards, is_war):
        """
        Checks to see if player has enough cards for reveal.
        Player needs atleast 3 cards for war. Atleast 1 for 
        normal reveal.

        Arguments:
            cards (tuple (num, suit)): Player's cards.
            is_war (bool): If war or not.

        Returns
            bool: if player has enough cards for war or reveal.
        """
        if not is_war and len(cards) > 0:
            return True
        elif is_war and len(cards) >= 3:
            return True
        else:
            return False

    def reveal_cards(self, is_war):
        """
        Reveal cards. Three for war, one for normal.

        Arguments:
            is_war (bool): If war or not.

        Returns:
            tuple ((num, suit), (num, suit)): player's reveal card.
        """
        if self.enough_cards(self.player.cards, is_war):
            player_card = self.player.reveal(is_war)
        else:
            player_card = None

        if self.enough_cards(self.hal.cards, is_war):
            hal_card = self.hal.reveal(is_war)
        else:
            hal_card = None

        return player_card, hal_card

    def get_battle_results(self, player_card, hal_card, active_cards):
        """
        Based on reveal cards, see if player 1 won, HAL won, or if war.

        Arguments:
            player_card (num, suit): players reveal card.
            hal_card (num, suit): HAL's reveal card.
            active_cards ([(num, suit)]): List of active cards.

        Returns:
            []: If a player won.
            [(num, suit)]: If war.
            None: If a player doesn't have enough cards for war.
        """
        if self.get_value(player_card) > self.get_value(hal_card):
            print(f"{self.player.name} wins this battle: +{len(active_cards)}")
            self.player.take(active_cards)
            return active_cards
        elif self.get_value(player_card) < self.get_value(hal_card):
            print(f"{self.hal.name} wins this battle: +{len(active_cards)}")
            self.hal.take(active_cards)
            return active_cards
        else:
            print("WAR!")
            print(
                f"{self.player.name} has {len(self.player.cards)} cards.".ljust(30), end='')
            print(f"{self.hal.name} has {len(self.hal.cards)} cards.".ljust(30))

            player_cards, hal_cards = self.reveal_cards(is_war=True)
            if player_cards is None or hal_cards is None:
                return None
            else:
                print(f"{self.player.name} -3.".ljust(30), end='')
                print(f"{self.hal.name} -3".ljust(30))
                return active_cards + player_cards + hal_cards

    def battle(self, active_cards):
        """
        Main battle function.

        Arguments:
            active_cards [(num, suit)]: list of cards on the board.

        Returns:
            bool: If the game should continue or not.
        """
        print(
            f"{self.player.name} has {len(self.player.cards)} cards.".ljust(30), end='')
        print(f"{self.hal.name} has {len(self.hal.cards)} cards.".ljust(30))
        if active_cards:
            print(f"There are {len(active_cards)} cards on the board.")

        player_card, hal_card = self.reveal_cards(is_war=False)
        if player_card is None or hal_card is None:
            return False
        active_cards += [player_card, hal_card]

        print(f"{self.player.name} -1.".ljust(30), end='')
        print(f"{self.hal.name} -1".ljust(30))
        print(f"Cards on Board {len(active_cards)}")
        print(
            f"{self.player.name}: {player_card[0]}-{player_card[1]}\tvs.\t{self.hal.name}: {hal_card[0]}-{hal_card[1]}")

        active_cards = self.get_battle_results(
            player_card, hal_card, active_cards)
        if active_cards == None:
            return False
        elif active_cards:
            print(f"Cards on Board {len(active_cards)}")
            return True and self.battle(active_cards)
        elif len(self.player.cards) == 0 or len(self.hal.cards) == 0:
            return False
        else:
            return True

    def start_game(self):
        """ Main game loop."""
        round_count = 1
        continue_game = True
        while continue_game is True:
            print(f"/////////////////////////////////////////////////////////////")
            print(f"ROUND {round_count}")
            print(f"/////////////////////////////////////////////////////////////")
            active_cards = []
            continue_game = self.battle(active_cards)
            round_count += 1

        print("GAME OVER")
        print("************************************************************")
        print(f"{self.get_winner()} is the WINNER")
        print("************************************************************")


def main_menu():
    """Get user name and start the war game."""
    print("Hello opponent. I am HAL. Welcome and lets go to WAR!")
    input("\nPress ENTER to begin")
    player_one_name = input("Please enter your name: ")

    deck = Deck()
    deck.shuffle()
    deck1, deck2 = deck.deal()

    game = WarGame(player_one_name, deck, deck1, deck2)
    game.start_game()


if __name__ == '__main__':
    main_menu()
