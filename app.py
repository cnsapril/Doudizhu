# coding=utf-8

from random import shuffle, randint

suit_symbol = [u'\u2663', u'\u2666', u'\u2665', u'\u2660', u"\U0001F0BF", u"\U0001F0CF"]


class Suits(object):
    """Enum class to represent the suit of the card"""
    clubs = 0
    diamonds = 1
    hearts = 2
    spades = 3
    b_joker = 4
    s_joker = 5


class Card(object):
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __cmp__(self, other):
        return self.value - other.value

    def __eq__(self, other):
        return self.value == other.value

    def __unicode__(self):
        if self.value <= 10:
            temp_value = str(self.value)
        else:
            switcher = {
                11: u"J",
                12: u"Q",
                13: u"K",
                14: u"A",
                15: u"2",
                16: u"小王",
                17: u"大王",
            }
            temp_value = switcher.get(self.value)

        return suit_symbol[self.suit] + temp_value


class Deck(object):
    def __init__(self):
        self.cards = []
        for suit in [Suits.clubs, Suits.diamonds, Suits.hearts, Suits.spades]:
            for value in xrange(3, 16):
                self.cards.append(Card(value, suit))
        self.cards.append(Card(16, Suits.s_joker))
        self.cards.append(Card(17, Suits.b_joker))
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
        print "底牌：",
        for i in xrange(3):
            temp_card = deck.draw()
            print temp_card,
            self.cards.append(temp_card)
        print

        if not deck.is_empty():
            print "Error assigning cards. Card is not empty after the operation! Exiting..."
            quit()

    def print_hand(self):
        self.cards.sort(reverse=True)
        print "你的手牌:",
        for current_card in self.cards:
            print current_card,
        print


class Player(object):
    def __init__(self, name):
        self.name = name
        self.is_winner = False
        self.hand = None

    def __str__(self):
        return unicode(self).encode("utf-8")

    def __unicode__(self):
        return self.name

    def be_landlord(self, deck):
        self.hand.take_bottom(deck)


class Game(object):
    def __init__(self):
        self.players = []
        self.deck = Deck()
        self.landlord = None

    def join(self, player):
        if len(self.players) > 3:
            print "本场游戏人数已满，请重新开始一轮新的游戏"
        else:
            self.players.append(player)
            print "玩家" + player.name + "加入游戏"

    def start(self):
        if len(self.players) < 3:
            print "斗地主需要3人才可进行，目前人数不足，游戏不能开始"
        else:
            landlord_pos = randint(0, 2)
            self.landlord = self.players[landlord_pos]
            for player in self.players:
                player.hand = Hand(self.deck)
                print "玩家" + player.name,
                player.hand.print_hand()
            current_pos = landlord_pos
            for i in range(3):
                current_pos = (current_pos + 1) % 3
                if raw_input("玩家" + self.players[current_pos].name + "：是否抢地主？") == 'y':
                    self.players[current_pos].be_landlord(self.deck)
                    print "本轮地主：" + self.landlord.name
                    print "地主" + self.landlord.name,
                    self.landlord.hand.print_hand()
                    break
            else:
                print "没有玩家选择当地主，游戏结束。请开始新一轮游戏。"


game = Game()
cqc = Player("陈倩偲")
cns = Player("陈凝霜")
szy = Player("石真玉")
game.join(cqc)
game.join(cns)
game.join(szy)
game.start()

