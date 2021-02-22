# Object class for a card player
# An actor has an hand (a collection of cards) and money

class Actor:

    def __init__(self):
        self.hand = []
        self.money = 100

    def add_card(self, new_card):
        if type(new_card) == type([]):
            self.hand.extend(new_card)
        else:
            self.hand.append(new_card)
        
    def discard(self):
        self.hand.clear()

    def get_hand(self):
        return self.hand

    def get_money(self):
        return self.money

    def add_money(self, amount):
        self.money = self.money + int(amount)
    
    def deduct_money(self, amount):
        self.money = self.money - int(amount)

    def hand_str(self, string):
        print(string)
        for card in self.hand:
            print(f'  {card.__str__()}')
