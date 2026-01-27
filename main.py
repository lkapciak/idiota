from core import *
from gui import *
from rules import *

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

pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Card Game")
font = pygame.font.SysFont(None, 36)

players, images, back_img = gui_init()
# [TO-DO] Let first player with the lowest card (not counting special cards) start by ordering player list

game = init_game(gui_player_names=players)


leaderboard = []

while game.players_count > 1:
    current_round, current_turn, current_player_turn = game.round, game.turn, game.player_turn
    current_player, current_hand = game.players[current_player_turn], game.hands[current_player_turn]
    current_table = game.table[-1] if game.table else None
    current_deck = game.deck

    serve_gui(screen, game, images, back_img) # Show current state
    
    # --------------- No legal moves --------------- #
    if not has_legal_moves(current_table, current_hand):
        
        # Last resort - draw 1 card (if eligible), see if it saves you
        if current_hand.count_cards('cards') == 3 and current_deck.cards_left() > 0: # last resort conditions
            last_resort = current_deck.draw(1)
            if is_legal(current_table, last_resort): # safe!
                game.update_table(last_resort)
            else: # not this time...
                current_hand.add_cards([last_resort]) # take last resort
                current_hand.add_cards(game.table) # and table contents
                game.discard_table()
                current_table = None
        
        # Last resort not possible
        else:
            # [TO-DO] Inform the player there are no legal moves [TO-DO]
            current_hand.add_cards(game.table) # Add all cards to current player's hand
            game.discard_table() # by removing all cards from the table
            game.next_turn()



    # --------------- Legal moves --------------- #
    else:
        # Choose a move
        # [TO-DO]
        is_choice_ready = False
        while not is_choice_ready:
            card_choice = None # [TO-DO]
            is_choice_ready = is_legal(current_table, card_choice) # Set is_choice_ready = True when the move is legal 
            # [TO-DO] check_multiple_cards_move()
        # [TO-DO]

        # Throw a card
        current_hand.remove_card(card_choice)
        game.update_table(card_choice)
        current_table = game.table[-1]

        # Draw until you have 3 cards if there are cards to be drawn
        if current_deck.cards_left() > 0 and current_hand.count_cards() < 3:
            current_hand.add_cards(
                current_deck.draw(
                    min(
                        3 - current_hand.count_cards(),
                        current_deck.cards_left() # if there aren't enough cards to draw, draw all left
                        )
                    )
                )

        # [TO-DO] check_multiple_cards_move()


    if current_table: # If the table is not empty
        if current_table.get_rank() == 10: # Check if the last card was a 10
            game.discard_table() # discard_table() if so
        else:
            game.check_last_four_cards() # Check if four card rule should be applied; discard_table() if so

    if is_player_winner(current_hand): # If one player won:
        winner_index = game.player_turn
        win_msg = current_player.player_win()
        # [TO-DO] Display the win message
        leaderboard.append((current_player.name, current_round))
        game.players.pop(winner_index)
        game.hands.pop(winner_index)
        game.player_turn %= game.players_count
        continue

    game.next_turn()

# Adding the last player to the leaderboard
leaderboard.append((game.players[0], 'LOSER!'))
# [TO-DO] Display leaderboard - player name, number of rounds it took to finish the game