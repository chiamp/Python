import random

class Card:
    def __init__(self,name):
        #argument name is type str
        self.name = name
        if name.isdigit():
            self.low_value,self.high_value = int(name),int(name)
        else:
            if name == 'A':
                self.low_value = 1
                self.high_value = 11
            else:
                self.low_value,self.high_value = 10,10
    def copy(self):
        return Card(self.name)
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
    def __gt__(self,other):
        return self.high_value > other.high_value
    def __lt__(self,other):
        return self.high_value < other.high_value
    def __ge__(self,other):
        return self.high_value >= other.high_value
    def __le__(self,other):
        return self.high_value <= other.high_value
    def __eq__(self,other):
        return self.high_value == other.high_value

class Hand:
    def __init__(self,hand):
        if len(hand) == 0 or type(hand[0]) == Card:
            self.hand = hand
        else:
            self.hand = [Card(s) for s in hand]
        self.a_card = Card('A')
    def add_card(self,card):
        self.hand.append(card)
    def get_high_value(self):
        #high_value = maximum one Ace being 11
        if self.a_card not in self.hand:
            total = 0
            for card in self.hand:
                total += card.high_value
            return total
        else:
            pre_total = 0
            num_a = 0
            for card in self.hand:
                if card != self.a_card:
                    pre_total += card.high_value
                else:
                    num_a += 1
            if 21-pre_total >= 11:
                pre_total += 11
                num_a -= 1
            return pre_total + num_a
    def get_low_value(self):
        #low_value = no Ace being 11; all Aces are 1's
        #if there are no Aces, then a low value doesn't exist; return 0
        if self.a_card not in self.hand:
            return 0
        else:
            total = 0
            for card in self.hand:
                total += card.low_value
            if total != self.get_high_value():
                return total
            else:
                return 0
    def copy(self):
        return Hand([card.copy() for card in self.hand])
    def __str__(self):
        return str(self.hand)
    def __repr__(self):
        return str(self.hand)

class Deck:
    def __init__(self,deck=[]):
        self.deck = deck
        self.a_card = Card('A')
        self.card_list = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
    def draw_top_card(self):
        return self.deck.pop(random.randint(0,len(self.deck)-1))
        #return self.deck.pop(0)
    def draw_top_cards(self,x):
        card_list = []
        for _ in range(x):
            card_list.append(self.draw_top_card())
        return card_list
    def shuffle(self):
        random.shuffle(self.deck)
    def add_card(self,card):
        self.deck.append(card)
        self.shuffle()
    def add_cards(self,card_list):
        for card in card_list:
            self.deck.append(card)
        self.shuffle()
    def clear_deck(self):
        self.deck.clear()
    def initiate_standard_deck(self):
        self.clear_deck()
        for card in self.card_list:
            for _ in range(4):
                self.deck.append(Card(card))
        self.shuffle()
    def initiate_list_deck(self,lst):
        self.clear_deck()
        for card in lst:
            self.deck.append(Card(card))
        self.shuffle()
    def initiate_random_deck(self):
        #initiate a random deck with anywhere between 0-4 of a particular card
        self.clear_deck()
        for card in self.card_list:
            for _ in range(random.randint(0,4)):
                self.deck.append(Card(card))
        self.shuffle()
    def initiate_deck_size(self,n):
        #maximum 52
        self.initiate_standard_deck()
        for _ in range(52-n):
            self.deck.pop(random.randint(0,len(self.deck)-1))
        self.shuffle()
    def get_features(self):
        feature_list = [0 for _ in range(10)] #format [2,3,4,...,9,10,A]
        #possibly include additional feature of deck size?
        for card in self.deck:
            if card == self.a_card:
                feature_list[-1] += 1
            else:
                feature_list[card.high_value-2] += 1
        #feature list shows probability of drawing that card
        ##feature_list = [i/len(self.deck) for i in feature_list]
        #return counts only because we need to factor in the hidden card of the dealer
        #we will divide and get the probability with the get_features function of the Game class
        return feature_list
    def copy(self):
        return Deck([card.copy() for card in self.deck])
    def __str__(self):
        return str(self.deck)
    def __repr__(self):
        return '['+str(len(self.deck))+']'
    def __contains__(self,item):
        for card in self.deck:
            if item == card:
                return True
        return False

if __name__ == '__main__':
    d = Deck()
    d.initiate_standard_deck()
    c = d.deck[0]
    h = Hand(d.deck[:3])
    h = Hand(['A','A','K','5'])
    
    
