from enum import Enum
import random

from rules import *

class Suit(Enum):
    HEARTS = "Hearts"
    DIAMONDS = "Diamonds"
    CLUBS = "Clubs"
    SPADES = "Spades"

class Rank(Enum):
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"
    ACE = "A"


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        suit_emoji = {
            'SPADES': '♠️',
            'CLUBS' : '♣️',
            'HEARTS': '♥️',
            'DIAMONDS': '♦️'
        }
        return f"{self.rank.value}{suit_emoji[self.suit.name]}"
    
    def get_rank(self):
        try:
            return int(self.rank.value)
        except:
            high_ranks = {'J' : 11,
                          'Q' : 12,
                          'K' : 13,
                          'A' : 14}
            return high_ranks[self.rank.value]
        


class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in Suit for rank in Rank]

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, n=1):
        drawn = []
        for _ in range(n):
            if len(self.cards) == 0:
                break
            drawn.append(self.cards.pop(0))
        return drawn if drawn else None

    def cards_left(self):
        return len(self.cards)

    def __str__(self):
        return str([card.__str__() for card in self.cards])


class Player:
    def __init__(self, player_name):
        self.name = player_name

    def __str__(self):
        return f"Player {self.name}"
    
    def player_win(self):
        return f"Player {self.name} wins!"
    

class Hand:
    def __init__(self, player):
        self.player = player
        self.cards = []

    def add_cards(self, cards):
        self.cards.extend(cards)

    def remove_card(self, card):
        if card in self.cards:
            self.cards.remove(card)
            return card
        return None

    def show(self):
        return [str(card) for card in self.cards]
    
    def count_cards(self):
        return len(self.cards)

    def __str__(self):
        return f"{self.player.name}'s hand: {self.show()}"


class Game:
    def __init__(self, player_names):
        self.players = [Player(name) for name in player_names]
        self.players_count = len(self.players)
        self.deck = Deck()
        self.deck.shuffle()
        self.hands = {player: Hand(player) for player in self.players}
        self.turn = 0
        self.table = []

    def deal(self, n=3):
        for player in self.players:
            self.hands[player].add_cards(self.deck.draw(n))

    def show_hands(self):
        for player in self.players:
            print(self.hands[player])

    def next_turn(self):
        self.turn = (self.turn + 1) % len(self.players)

    def discard_table(self):
        self.table.clear()

    def check_last_four_cards(self):
        if last_four_cards_rule(self.table):
            self.discard_table()
