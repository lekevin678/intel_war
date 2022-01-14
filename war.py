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

    def reveal(self, is_war):
        if is_war:
            cards = []
            for _ in range(3):
                cards.append(self.cards.pop())
            return cards
        else:
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

    def enough_cards(self, cards, is_war):
        if not is_war and len(cards) > 0:
            return True
        elif is_war and len(cards) >= 3:
            return True
        else:
            return False

    def battle(self, active_cards):
        print(f"{self.player.name} has {len(self.player.cards)} cards.", end='')
        print(f"\t {self.hal.name} has {len(self.hal.cards)} cards.")

        if self.enough_cards(self.player.cards, is_war=False):
            player_card = self.player.reveal(is_war=False)
        else:
            print(f"{self.player.name} ran out of cards.")
            return False
        if self.enough_cards(self.hal.cards, is_war=False):
            hal_card = self.hal.reveal(is_war=False)
        else:
            print(f"{self.hal.name} ran out of cards.")
            return False

        print("Cards on Board +2")
        active_cards += [player_card, hal_card]

        if self.get_value(player_card) > self.get_value(hal_card):
            print(f"{self.player.name} wins this battle.")
            self.player.take(active_cards)
            return True
        elif self.get_value(player_card) < self.get_value(hal_card):
            print(f"{self.hal.name} wins this battle.")
            self.hal.take(active_cards)
            return True
        else:
            print("WAR!")
            if self.enough_cards(self.player.cards, is_war=True):
                player_cards = self.player.reveal(is_war=True)
            else:
                print(f"{self.player.name} ran out of cards for war.")
                return False
            if self.enough_cards(self.hal.cards, is_war=True):
                hal_cards = self.hal.reveal(is_war=True)
            else:
                print(f"{self.hal.name} ran out of cards for war.")
                return False

            print("Cards on Board +6")
            active_cards += player_cards + hal_cards
            return True and self.battle(active_cards)

    def main_loop(self):
        round_count = 1
        while len(self.player.cards) > 0 and len(self.hal.cards) > 0:
            print(f"/////////////////////////////////////////////////////////////")
            print(f"ROUND {round_count}")
            print(f"/////////////////////////////////////////////////////////////")
            active_cards = []
            continue_game = self.battle(active_cards)
            if not continue_game:
                break
            round_count += 1

        print("GAME OVER")


def start_game():
    print("Hello opponent. I am HAL. Welcome and lets go to WAR!")
    input("\nPress ENTER to begin")
    player_one_name = input("Please enter your name: ")

    game = WarGame(player_one_name)
    game.main_loop()


start_game()
