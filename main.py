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


screen, players, images, back_img = gui_init()
game = init_game(players)

leaderboard = []

while game.players_count > 1:
    current_round, current_turn, current_player_turn = game.round, game.turn, game.player_turn
    current_player, current_hand = game.players[current_player_turn], game.hands[current_player_turn]
    current_table = game.table[-1] if game.table else None
    current_deck = game.deck
    # --------------- No legal moves --------------- #
    if not has_legal_moves(current_table, current_hand):

        # Last resort - draw 1 card (if eligible)
        if current_hand.count_cards('cards') == 3 and current_deck.cards_left() > 0:
            last_resort = current_deck.draw(1)[0]

            # Display drawn card for 3 seconds
            show_temporary_message(
                screen=screen,
                game=game,
                images=images,
                back_img=back_img,
                message_lines=[
                    f"{current_player.name} dobiera pierwszą kartę...",
                    f"Sprawdzamy, czy można ją zagrać."
                ],
                duration_ms=3000,
                extra_card=last_resort,
                active_player_idx=current_player_turn
            )

            if is_legal(current_table, last_resort):  # safe!
                game.update_table(last_resort)

                show_temporary_message(
                    screen=screen,
                    game=game,
                    images=images,
                    back_img=back_img,
                    message_lines=[
                        f"{current_player.name} został uratowany!",
                        f"Karta {last_resort} została automatycznie zagrana."
                    ],
                    duration_ms=2000,
                    active_player_idx=current_player_turn
                )

            else:  # not this time...
                current_hand.add_cards([last_resort])
                current_hand.add_cards(game.table)
                game.discard_table()
                current_table = None

                show_temporary_message(
                    screen=screen,
                    game=game,
                    images=images,
                    back_img=back_img,
                    message_lines=[
                        f"{current_player.name} nie ma legalnego ruchu."
                    ],
                    duration_ms=3000,
                    active_player_idx=current_player_turn
                )

                game.next_turn()
                continue

        # Last resort not possible
        else:
            show_temporary_message(
                screen=screen,
                game=game,
                images=images,
                back_img=back_img,
                message_lines=[
                    f"{current_player.name} nie ma legalnego ruchu.",
                ],
                duration_ms=2500,
                active_player_idx=current_player_turn
            )

            current_hand.add_cards(game.table)  # Add all cards to current player's hand
            game.discard_table()                # by removing all cards from the table
            game.next_turn()
            continue


    # --------------- Legal moves --------------- #
    else:
        is_choice_ready = False
        while not is_choice_ready:
            cards_to_play = choose_cards_via_gui(
                screen=screen,
                game=game,
                images=images,
                back_img=back_img,
                current_hand=current_hand,
                current_table=current_table,
                player_index=current_player_turn,
                is_legal=is_legal
            )

            card_choice = cards_to_play[0]
            is_choice_ready = is_legal(current_table, card_choice) # Set is_choice_ready = True when the move is legal 

        # Throw a card
        for card in cards_to_play:
            current_hand.remove_card(card)
            game.update_table(card)
        current_table = game.table[-1]

        # Draw until you have 3 cards if there are cards to be drawn
        if current_deck.cards_left() > 0 and current_hand.count_cards('cards') < 3:
            current_hand.add_cards(
                current_deck.draw(
                    min(
                        3 - current_hand.count_cards('cards'),
                        current_deck.cards_left() # if there aren't enough cards to draw, draw all left
                        )
                    ),
                    'cards'
                )

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
leaderboard.append((game.players[0].name, 'LOSER!'))
# [TO-DO] Display leaderboard - player name, number of rounds it took to finish the game