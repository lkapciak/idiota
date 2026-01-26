def last_four_cards_rule(table):
    try:
        for i in range(3):
            if table[i] != table[i+1]:
                return False 
        return True
    except: return False

def is_game_over(hands):
    for hand in hands:
        if hand.count_cards('cards') + hand.count_cards('hidden_cards') + hand.count_cards('open_cards') == 0:
            print(f"{str(hand.player)} wins!")
            return True
    return False

def is_legal(table, card):
    last_table_card = table[-1]
    if card.get_rank() in [2, 5, 10]:
        return True
    if last_table_card.get_rank() == 5:
        return card < last_table_card    
    else: return last_table_card < card     