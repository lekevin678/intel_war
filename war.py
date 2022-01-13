import random


class Deck ():
    nums = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    suits = ["S", "C", "D", "H"]
    deck = []

    def __init__(self):
        for num in self.nums:
            for suit in self.suits:
                self.deck.append((num, suit))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        half = int(len(self.deck)/2)
        return (self.deck[:half], self.deck[half:])


class Player():
    name = "DEFAULT"
    cards = []

    def __init__(self, name, deck):
        self.name = name
        self.cards = deck

    def reveal(self):
        return self.cards.pop()

    def take(self, active_cards):
        self.cards = active_cards + self.cards


class WarGame():
    deck = []

    def __init__(self, player_name):
        self.deck = Deck()
        self.deck.shuffle()
        deck1, deck2 = self.deck.deal()

        self.player = Player(player_name, deck1)
        self.hal = Player("HAL", deck2)

    def get_value(self, card):
        return self.deck.nums.index(card[0])

    def battle(self):
        active_cards = []
        player_card = self.player.reveal()
        hal_card = self.hal.reveal()
        active_cards += [player_card, hal_card]

        if self.get_value(player_card) > self.get_value(hal_card):
            self.player.take(active_cards)
        elif self.get_value(player_card) < self.get_value(hal_card):
            self.hal.take(active_cards)
        else:
            print("WAR")

    def main_loop(self):
        while len(self.player.cards) > 0 and len(self.hal.cards) > 0:
            print(f"Player has {len(self.player.cards)} cards.")
            print(f"HAL has {len(self.hal.cards)} cards.")
            self.battle()


def start_game():
    print("Hello opponent. I am HAL. Welcome and lets go to WAR!")
    input("\nPress ENTER to begin")
    player_one_name = input("Please enter your name: ")

    game = WarGame(player_one_name)
    game.main_loop()


start_game()
