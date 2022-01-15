"""Unit tests for war.py"""
import unittest
import sys
from war import Deck, Player, WarGame


class TestDeck(unittest.TestCase):
    """Unit tests for Deck class"""

    def setUp(self):
        self.deck = Deck()

    def test_init(self):
        for num in self.deck.nums:
            for suit in self.deck.suits:
                self.assertIn((num, suit), self.deck.deck)

    def test_deal(self):
        deck1, deck2 = self.deck.deal()
        self.assertEqual(len(deck1), 26)
        self.assertEqual(len(deck2), 26)


class TestPlayer(unittest.TestCase):
    """Unit tests for Player class"""

    def setUp(self):
        self.player = Player(
            "unittest", [('2', 'S'), ('3', 'S'), ('4', 'S'), ('5', 'S')])

    def test_reveal_not_war(self):
        reveal_card = self.player.reveal(is_war=False)
        self.assertEqual(reveal_card, ('5', 'S'))
        self.assertEqual(self.player.cards, [
                         ('2', 'S'), ('3', 'S'), ('4', 'S')])

    def test_reveal_war(self):
        reveal_card = self.player.reveal(is_war=True)
        self.assertEqual(reveal_card, [
                         ('5', 'S'), ('4', 'S'), ('3', 'S')])
        self.assertEqual(self.player.cards, [('2', 'S')])

    def test_take(self):
        active_cards = [('2', 'C'), ('3', 'C')]
        self.player.take(active_cards)
        self.assertEqual(self.player.cards, [
                         ('2', 'C'), ('3', 'C'), ('2', 'S'), ('3', 'S'), ('4', 'S'), ('5', 'S')])


class TestWar(unittest.TestCase):
    """Unit tests for War class"""

    def test_get_winner(self):
        deck = Deck()
        deck.shuffle()
        winner_cards = [('2', 'S'), ('3', 'S'), ('4', 'S'), ('5', 'S')]
        loser_cards = [('2', 'C')]
        no_cards = []

        game = WarGame("unittest", deck, winner_cards, loser_cards)
        self.assertEqual(game.get_winner(), "unittest")

        game = WarGame("unittest", deck, no_cards, winner_cards)
        self.assertEqual(game.get_winner(), "HAL")

    def test_get_value(self):
        deck = Deck()
        deck.shuffle()
        deck1, deck2 = deck.deal()

        game = WarGame("unittest", deck, deck1, deck2)

        self.assertEqual(game.get_value(('2', 'S')), 0)
        self.assertEqual(game.get_value(('2', 'H')), 0)
        self.assertEqual(game.get_value(('10', 'H')), 8)
        self.assertEqual(game.get_value(('Q', 'H')), 10)
        self.assertEqual(game.get_value(('A', 'H')), 12)

    def test_enough_cards(self):
        deck = Deck()
        deck.shuffle()
        deck1, deck2 = deck.deal()

        cards_3 = [('2', 'S'), ('3', 'S'), ('4', 'S')]
        cards_1 = [('2', 'S')]
        cards_0 = []

        game = WarGame("unittest", deck, deck1, deck2)

        self.assertTrue(game.enough_cards(cards_3, is_war=False))
        self.assertTrue(game.enough_cards(cards_1, is_war=False))
        self.assertFalse(game.enough_cards(cards_0, is_war=False))

        self.assertTrue(game.enough_cards(cards_3, is_war=True))
        self.assertFalse(game.enough_cards(cards_1, is_war=True))
        self.assertFalse(game.enough_cards(cards_0, is_war=True))

    def test_reveal_cards(self):
        deck = Deck()
        deck.shuffle()

        cards_1 = [('2', 'S'), ('3', 'S'), ('4', 'S')]
        cards_2 = [('2', 'C'), ('3', 'C'), ('4', 'C')]

        game1 = WarGame("unittest", deck, cards_1, cards_2)

        # Reveal a card
        player_card, hal_card = game1.reveal_cards(is_war=False)
        self.assertEqual(player_card, ('4', 'S'))
        self.assertEqual(hal_card, ('4', 'C'))

        # Reveal War but not enough
        player_card, hal_card = game1.reveal_cards(is_war=True)
        self.assertEqual(player_card, None)
        self.assertEqual(hal_card, None)

        # Reveal War
        cards_3 = [('2', 'S'), ('3', 'S'), ('4', 'S'), ('A', 'S')]
        cards_4 = [('2', 'C'), ('3', 'C'), ('4', 'C'), ('A', 'C')]
        game2 = WarGame("unittest", deck, cards_3, cards_4)
        player_card, hal_card = game2.reveal_cards(is_war=True)
        self.assertEqual(player_card, [('A', 'S'), ('4', 'S'), ('3', 'S')])
        self.assertEqual(hal_card, [('A', 'C'), ('4', 'C'), ('3', 'C')])

    def test_get_battle_results(self):
        deck = Deck()
        deck.shuffle()
        player_cards = [('2', 'S'), ('2', 'C')]
        hal_cards = [('2', 'D'), ('2', 'H')]
        game = WarGame("unittest", deck, player_cards, hal_cards)

        # HAL wins
        player_card = ('3', 'S')
        hal_card = ('4', 'C')
        active_cards = [('3', 'S'), ('4', 'C')]
        cards = game.get_battle_results(player_card, hal_card, active_cards)
        self.assertEqual(cards, [])
        self.assertEqual(len(game.hal.cards), 4)
        self.assertEqual(len(game.player.cards), 2)

        # Player wins
        player_card = ('6', 'S')
        hal_card = ('5', 'C')
        active_cards = [('6', 'S'), ('5', 'C')]
        cards = game.get_battle_results(player_card, hal_card, active_cards)
        self.assertEqual(cards, [])
        self.assertEqual(len(game.hal.cards), 4)
        self.assertEqual(len(game.player.cards), 4)

        # War
        player_card = ('10', 'S')
        hal_card = ('10', 'C')
        active_cards = [('10', 'S'), ('10', 'C')]
        cards = game.get_battle_results(player_card, hal_card, active_cards)
        self.assertEqual(cards, [('10', 'S'), ('10', 'C'), ('2', 'C'),
                                 ('2', 'S'), ('5', 'C'), ('2', 'H'), ('2', 'D'), ('4', 'C')])
        self.assertEqual(len(game.hal.cards), 1)
        self.assertEqual(len(game.player.cards), 1)

        # War (Not Enough Cards)
        player_card = ('10', 'S')
        hal_card = ('10', 'C')
        active_cards = [('10', 'S'), ('10', 'C')]
        cards = game.get_battle_results(player_card, hal_card, active_cards)
        self.assertEqual(cards, None)
        self.assertEqual(len(game.hal.cards), 1)
        self.assertEqual(len(game.player.cards), 1)

    def test_battle(self):
        deck = Deck()
        deck.shuffle()

        # Not Enough Cards for War
        player_cards = [('2', 'S'), ('2', 'C')]
        hal_cards = [('2', 'D'), ('2', 'H')]
        game1 = WarGame("unittest", deck, player_cards, hal_cards)
        self.assertFalse(game1.battle([]))

        # Not Enough Cards for initial reveal
        player_cards = []
        hal_cards = []
        game1 = WarGame("unittest", deck, player_cards, hal_cards)
        self.assertFalse(game1.battle([]))

        # War
        player_cards = [('10', 'S'), ('2', 'S'),
                        ('2', 'C'), ('3', 'S'), ('3', 'C')]
        hal_cards = [('9', 'S'), ('2', 'D'), ('2', 'H'),
                     ('3', 'D'), ('3', 'H')]
        game1 = WarGame("unittest", deck, player_cards, hal_cards)
        self.assertTrue(game1.battle([]))

        # War 2X
        player_cards = [('J', 'S'), ('4', 'S'), ('4', 'C'), ('5', 'S'), ('10', 'S'),
                        ('2', 'S'), ('2', 'C'), ('3', 'S'), ('3', 'C')]
        hal_cards = [('7', 'S'), ('4', 'D'), ('4', 'H'), ('5', 'D'), ('10', 'C'),
                     ('2', 'D'), ('2', 'H'), ('3', 'D'), ('3', 'H')]
        game1 = WarGame("unittest", deck, player_cards, hal_cards)
        self.assertTrue(game1.battle([]))

        # War 2X, HAL not enough cards
        player_cards = [('7', 'S'), ('4', 'S'), ('4', 'C'), ('5', 'S'), ('10', 'S'),
                        ('2', 'S'), ('2', 'C'), ('3', 'S'), ('3', 'C')]
        hal_cards = [('4', 'D'), ('4', 'H'), ('5', 'D'), ('10', 'C'),
                     ('2', 'D'), ('2', 'H'), ('3', 'D'), ('3', 'H')]
        game1 = WarGame("unittest", deck, player_cards, hal_cards)
        self.assertFalse(game1.battle([]))


if __name__ == '__main__':
    unittest.main()
