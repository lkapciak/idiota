from core import *

def last_four_cards_rule(table: list) -> bool:
    """
    Checks if last four cards rule should be invoked.

    The *last four cards rule* states that if four cards of the same value are placed directly on top of each other, all table cards shall be discarded (as if a 10 was placed).
    
    :param list of Cards table: Table history.
    """
    try:
        for i in range(3):
            if table[i] != table[i+1]:
                return False 
        return True
    except: return False

def is_player_winner(hand: Hand) -> bool:
    """
    Determines whether a player has won.
    
    :param Hand object hand: Player's card.
    """
    if hand.count_cards('cards') + hand.count_cards('hidden_cards') + hand.count_cards('open_cards') == 0:
        print(f"{str(hand.player)} wins!")
        return True
    return False

def is_legal(table: list, card: Card) -> bool:
    """
    Determines a card could be played with current table state.
    
    :param list of Cards table: Table history.
    :param Card object card: Player's card.
    """
    if table:
        last_table_card = table[-1]
        if card.get_rank() in [2, 5, 10]:
            return True
        if last_table_card.get_rank() == 5:
            return card < last_table_card    
        else: return last_table_card < card     
    return True

def has_legal_moves(table: list, hand: Hand) -> bool:
    """
    Determines whether any card from a hand could be played with current table state.
    
    :param list of Cards table: Table history.
    :param Hand object hand: Player's hand.
    """
    if hand.cards:
        active_cards = hand.cards
    elif hand.open_cards:
        active_cards = hand.open_cards
    else:
        active_cards = hand.hidden_cards

    return any(is_legal(table, card) for card in active_cards)