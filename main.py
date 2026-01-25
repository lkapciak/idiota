from core import *
from gui import *

def init_game(gui_player_names):
    
    def prepare_players(gui_player_names):
        return [Player(name) for name in gui_player_names]


    def prepare_deck(players):
        needed_decks = len(players) * 9 // 52 + 1
        deck = Deck()
        deck.extend_deck(needed_decks - 1)
        deck.shuffle()
        return deck

    def prepare_hands(players, deck):
        hands = [Hand(player) for player in players]
        for hand in hands:
            for pile in ['cards', 'hidden_cards', 'open_cards']:
                hand.add_cards(deck.draw(3), pile)
        return hands
    
    
    players = prepare_players(gui_player_names)
    deck = prepare_deck(players)
    hands = prepare_hands(players, deck)
    game = Game(players, deck, hands)
    return game


gui_player_names = gui_init()
game = init_game(gui_player_names)
players = game.players

while not is_game_over(game.hands):
    
    

    game.check_last_four_cards()
    game.next_turn()