# coding=utf-8

from random import shuffle


class Suits(object):
    """Enum class to represent the suit of the card"""
    clubs = 0
    diamonds = 1
    hearts = 2
    spades = 3
    b_joker = 4
    s_joker = 5

suit_symbol = [u'\u2663', u'\u2666', u'\u2665', u'\u2660']


class Card(object):
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __repr__(self):
        return suit_symbol[self.suit] + str(self.value)


class Deck(object):
    def __init__(self):
        self.cards = []
        for suit in [Suits.clubs, Suits.diamonds, Suits.hearts, Suits.spades]:
            for value in xrange(1, 14):
                self.cards.append(Card(value, suit))
        self.cards.append(Card(14, Suits.s_joker))
        self.cards.append(Card(15, Suits.b_joker))
        shuffle(self.cards)

    def draw(self):
        if len(self.cards) <= 0:
            return None
        return self.cards.pop()

    def is_empty(self):
        return not self.cards


class Hand(object):
    def __init__(self, deck):
        self.cards = []
        for i in xrange(17):
            self.cards.append(deck.draw())

    def take_bottom(self, deck):
        for i in xrange(3):
            self.cards.append(deck.draw())

        if not deck.is_empty():
            print "Error assigning cards. Card is not empty after the operation! Exiting..."
            quit()

    def print_hand(self):
        print "你的手牌:",
        for card in self.cards:
            print card


card = Card(7, Suits.clubs)
print card
