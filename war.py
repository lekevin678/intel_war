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

    def take(self, cards):
        self.cards.insert(0, cards)


class WarGame():
    deck = []

    def __init__(self):
        print("Hello opponent. I am HAL. Welcome and lets go to WAR!")
        input("\nPress ENTER to begin")
        player_one_name = input("Please enter your name: ")

        self.deck = Deck()
        self.deck.shuffle()
        deck1, deck2 = self.deck.deal()

        self.player = Player(player_one_name, deck1)
        self.hal = Player("HAL", deck2)

    def main_loop(self):
        while len(self.player.cards) > 0 and len(self.hal.cards) > 0:
            print(f"Player has {len(self.player.cards)} cards.")
            print(f"HAL has {len(self.hal.cards)} cards.")


game = WarGame()
game.main_loop()
