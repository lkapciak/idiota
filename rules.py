def last_four_cards_rule(table):
    try:
        for i in range(3):
            if table[i] != table[i+1]:
                return False 
        return True
    except: return False