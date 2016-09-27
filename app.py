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
            print "发牌出现错误，发完牌后牌堆仍然有牌。退出中..."
            quit()

    def print_hand(self):
        self.cards.sort(reverse=True)
        print "你的手牌:",
        for current_card in self.cards:
            print current_card,
        print


class CardPlay(object):
    def __init__(self, play_str):
        self.cards = []
        self.is_shunzi = False
        self.is_3dai1 = False
        self.is_feiji = False
        self.is_zhadan = False
        self.is_duizi = False
        self.is_danzhang = False
        self.is_banzipao = False
        self.is_4dai2 = False
        self.invalid = False

        __switcher = {
            '1': 10,
            '2': 15,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            'J': 11,
            'Q': 12,
            'K': 13,
            'A': 14,
            's': 16,
            'b': 17,
        }

        for card_chr in play_str:
            if card_chr != '0':
                self.cards.append(Card(__switcher.get(card_chr), Suits.clubs))
        self.cards.sort()

        length = len(self.cards)
        if length >= 5:
            # 检查是否为顺子
            for i in xrange(1, length):
                card = self.cards[i]
                pre_card = self.cards[i-1]
                if card.value != pre_card.value + 1 or card.value > __switcher.get('A'):
                    break
            else:
                self.is_shunzi = True
                return

            # 检查是否为板子炮
            for i in xrange(0, length-2, 2):
                if self.cards[i] != self.cards[i+1] or self.cards[i].value + 1 != self.cards[i+2].value:
                    break
            else:
                self.is_banzipao = True
                return

            # 检查是否为飞机
            card_dict = {}
            for card in self.cards:
                if card.value in card_dict:
                    card_dict[card.value] += 1
                else:
                    card_dict[card.value] = 1

            three_count = 0
            one_count = 0
            four_count = 0
            for key in card_dict:
                if card_dict[key] == 3:
                    three_count += 1
                elif card_dict[key] == 4:
                    four_count += 1
                else:
                    one_count += card_dict[key]

            if three_count == one_count:
                self.is_feiji = True
                return

            # 检查是否为四带二
            if four_count * 2 == one_count:
                self.is_4dai2 = True
                return

        elif length == 4:
            # 检查是否为炸弹
            if self.cards[0] == self.cards[1] == self.cards[2] == self.cards[3]:
                self.is_zhadan = True
                return

            # 检查是否为三带一
            elif self.cards[0] == self.cards[1] == self.cards[2] or self.cards[1] == self.cards[2] == self.cards[3]:
                self.is_3dai1 = True
                return

        elif length == 2:
            # 检查是否是王炸
            if (self.cards[0].value == __switcher.get('s') and self.cards[1].value == __switcher.get('b')) or \
                    (self.cards[0].value == __switcher.get('b') and self.cards[1].value == __switcher.get('s')):
                self.is_zhadan = True
                return

            # 检查是否是对子
            elif self.cards[0] == self.cards[1]:
                self.is_duizi = True
                return

        elif length == 1:
            # 检查是否是单张
            self.is_danzhang = True
            return

        self.invalid = True

    def validate(self, hand):
        """检查出的牌是否合法"""

        # 检查出的牌是不是基础牌型之一
        if self.invalid:
            return False

        # 检查出的牌手中有没有
        card_dict = {}
        for card in hand.cards:
            if card.value not in card_dict:
                card_dict[card.value] = 1
            else:
                card_dict[card.value] += 1

        for played_card in self.cards:
            if played_card.value not in card_dict:
                return False
            elif card_dict[played_card.value] <= 0:
                return False
            else:
                card_dict[played_card.value] -= 1

        return True




# play = CardPlay('444423')
# print "顺子：" + str(play.is_shunzi)
# print "飞机：" + str(play.is_feiji)
# print "炸弹：" + str(play.is_zhadan)
# print "三带一：" + str(play.is_3dai1)
# print "板子炮：" + str(play.is_banzipao)
# print "单张：" + str(play.is_danzhang)
# print "对子：" + str(play.is_duizi)
# print "四带二：" + str(play.is_4dai2)


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

    def has_no_card(self):
        return len(self.hand.cards) == 0

    def show_hand(self):
        self.hand.print_hand()

    def play(self, last_play):
        while True:
            cards_str = raw_input("请输入你要出的牌：")
            current_play = CardPlay(cards_str)
            if current_play.validate(self.hand):
                # if current_play > last_play:
                #     return current_play
                print "你出的牌是合法的"
                return current_play
            else:
                print "出牌不合法，重新出牌"


class Game(object):
    def __init__(self):
        self.players = []
        self.__deck = Deck()
        self.landlord = None
        self.winner = None

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
                player.hand = Hand(self.__deck)
                print "玩家" + player.name,
                player.show_hand()
            current_pos = landlord_pos
            for i in range(3):
                if raw_input("玩家" + self.players[current_pos].name + "：是否抢地主？") == 'y':
                    self.players[current_pos].be_landlord(self.__deck)
                    print "本轮地主：" + self.landlord.name
                    print "地主" + self.landlord.name,
                    self.landlord.show_hand()
                    break
                current_pos = (current_pos + 1) % 3
            else:
                print "没有玩家选择当地主，游戏结束。请开始新一轮游戏。"
                return

            self.__main_loop()

    def __main_loop(self):
        current_player = self.landlord
        last_play = None
        while self.winner is None:
            print "轮到" + current_player.name + "出牌"
            last_play = current_player.play(last_play)
            if current_player.has_no_card():
                self.winner = current_player
                if self.winner == self.landlord:
                    print "游戏结束，地主获胜！"
                else:
                    print "游戏结束，农民获胜！"
            current_player = self.players[(self.players.index(current_player) + 1) % 3]

game = Game()
cqc = Player("陈倩偲")
cns = Player("陈凝霜")
szy = Player("石真玉")
game.join(cqc)
game.join(cns)
game.join(szy)
game.start()

