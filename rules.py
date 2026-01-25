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