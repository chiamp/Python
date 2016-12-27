from container import Container

class Card:
    '''Class for playing Cards'''
    def __init__(self, value, suit):
        self.order = [[2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'],['D', 'C', 'H', 'S']]
        #assert value.upper() in self.order[0] if type(value) == str else value in self.order[0]
        assert suit.upper() in self.order[1]
        self.suit = suit.upper()
        if type(value) == str:
            self.value = value.upper()
        else:
            self.value = value
    def __repr__(self):
        return '{}{}'.format(self.value, self.suit)
    def __str__(self):
        return '{}{}'.format(self.value, self.suit)
    def __eq__(self, other):
        return self.value == other.value #and self.suit == other.suit
    def __gt__(self, other):
        return self.order[0].index(self.value) > self.order[0].index(other.value) #if self.value != other.value else self.order[1].index(self.suit) > self.order[1].index(other.suit)
    def __lt__(self, other):
        return self.order[0].index(self.value) < self.order[0].index(other.value) #if self.value != other.value else self.order[1].index(self.suit) < self.order[1].index(other.suit)
    def __ge__(self, other):
        return self.order[0].index(self.value) >= self.order[0].index(other.value) #if self.value != other.value else self.order[1].index(self.suit) >= self.order[1].index(other.suit)
    def __le__(self, other):
        return self.order[0].index(self.value) <= self.order[0].index(other.value) #if self.value != other.value else self.order[1].index(self.suit) <= self.order[1].index(other.suit)
        
class Deck(Container):
    '''Class Deck to store class Cards'''
    def __init__(self):
        '''Initializes class Deck. Left most side of the deck list represents the top of the deck.
        @type self: Deck
        @type self.deck: list[Card]
        '''
        Container.__init__(self)
        #self.deck = self.container
        self.order = [['A', 'K', 'Q', 'J', 10, 9, 8, 7, 6, 5, 4, 3, 2],['S', 'H', 'C', 'D']]
        self.discard = []
    def __str__(self):
        return '{}'.format(self.container)
    def __repr__(self):
        return '{}'.format(self.container)
    def new_deck_suit(self):
        '''Fills self.deck with all 52 playing Cards in order from highest suit to lowest suit.'''
        self.container.clear()
        for suit in self.order[1]:
            for value in self.order[0]:
                self.container.append(Card(value, suit))
    def new_deck_value(self):
        '''Fills self.deck with all 52 playing Cards in order from highest number to lowest number.'''
        self.container.clear()
        for value in self.order[0]:
            for suit in self.order[1]:
                self.container.append(Card(value, suit))
    #def add_cards(self, card_list):
    #    self.deck.append_group(card_list)
    #def add_cards_top(self, card_list):
    #    self.deck.append_left_group(card_list)

def hand_score(hand):
    '''Evaluates the hand value. Hand must be length 5.
    @type hand: list[Card]
    @rtype: float
    
    Rankings:
    Straight flush - 9
    Four of a kind - 8
    Full house - 7
    Flush - 6
    Straight - 5
    Three of a kind - 4
    Two pair - 3
    One pair - 2
    High card - 1

    Primary kicker:
    A - 0.13
    .
    .
    .
    2 - 0.01

    Secondary kicker:
    K - 0.0012
    .
    .
    .
    2 - 0.0001
    '''
    assert len(hand) == 5
    order = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
    temp_hand = hand[:]
    temp_hand.sort() #sorted from lowest to highest
    if order.index(temp_hand[4].value) - order.index(temp_hand[3].value) == 1 and order.index(temp_hand[3].value) - order.index(temp_hand[2].value) == 1 and order.index(temp_hand[2].value) - order.index(temp_hand[1].value) == 1 and order.index(temp_hand[1].value) - order.index(temp_hand[0].value) == 1:
        if temp_hand[4].suit == temp_hand[3].suit == temp_hand[2].suit == temp_hand[1].suit == temp_hand[0].suit:
            return 90000000000 + order.index(temp_hand[4].value)*100000000 + 100000000
        else:
            return 50000000000 + order.index(temp_hand[4].value)*100000000 + 100000000
    if temp_hand[4].suit == temp_hand[3].suit == temp_hand[2].suit == temp_hand[1].suit == temp_hand[0].suit: #all suits same, but not in order
        return 60000000000 + order.index(temp_hand[4].value)*100000000 + 100000000

    multiple_dict = {} #{card.value: list[Card]}
    for card in temp_hand:
        if card.value not in multiple_dict:
            multiple_dict[card.value] = [card]
        else:
            multiple_dict[card.value].append(card)
            
    max_counter = [0, None, temp_hand] #[copies of value, Card, kicker]
    for key in multiple_dict:
        if max_counter[0] < len(multiple_dict[key]): #finding the highest number of copies of a single card
            max_counter[0], max_counter[1] = len(multiple_dict[key]), multiple_dict[key][0] #pick the first item in the key; doesn't really matter because they should have the same value
    if max_counter[0] == 4:
        new_dict = multiple_dict.copy()
        new_dict.pop(max_counter[1].value)
        temp_hand2 = []
        for key in new_dict:
            temp_hand2.append(new_dict[key][0])
        return 80000000000 + order.index(max_counter[1].value)*100000000 + 100000000 + order.index(temp_hand2[0].value)*1000000 + 1000000
    if max_counter[0] == 3:
        new_dict = multiple_dict.copy()
        new_dict.pop(max_counter[1].value)
        temp_hand2 = []
        for key in new_dict:
            temp_hand2.append(new_dict[key][0])
        if len(multiple_dict) == 2: #meaning there are only two entries for the card.value keys; meaning that if one of them is length 3, the other one must be length 2
            return 70000000000 + order.index(max_counter[1].value)*100000000 + 100000000 + order.index(temp_hand2[0].value)*1000000 + 1000000
        else:
            temp_hand2.sort()
            return 40000000000 + order.index(max_counter[1].value)*100000000 + 100000000 + order.index(temp_hand2[1].value)*1000000 + 1000000 + order.index(temp_hand2[0].value)*10000 + 10000
    if max_counter[0] == 2:
        if len(multiple_dict) == 4: #meaning it's only a one pair
            new_dict = multiple_dict.copy()
            new_dict.pop(max_counter[1].value)
            temp_hand2 = [] #list[Card]
            for key in new_dict: #only kickers remaining
                temp_hand2.append(new_dict[key][0])
            assert len(temp_hand2) == 3
            temp_hand2.sort()
            return 20000000000 + order.index(max_counter[1].value)*100000000 + 100000000 + order.index(temp_hand2[2].value)*1000000 + 1000000 + order.index(temp_hand2[1].value)*10000 + 10000 + order.index(temp_hand2[0].value)*100 + 100
        else: #meaning there is two pair
            highest_value = Card(2, 'D') #lowest card possible
            for key in multiple_dict:
                if len(multiple_dict[key]) == 2:
                    if multiple_dict[key][0] > highest_value:
                        highest_value = multiple_dict[key][0]
            new_dict = multiple_dict.copy()
            new_dict.pop(highest_value.value)
            for key in new_dict: #do it a second time to find second pair
                if len(new_dict[key]) == 2:
                    second_pair = new_dict[key][0]
            final_dict = new_dict.copy() #dictionary containing remaining kicker
            final_dict.pop(second_pair.value)
            temp_hand2 = []
            for key in final_dict: #only kickers remaining
                temp_hand2.append(final_dict[key][0])
            return 30000000000 + order.index(highest_value.value)*100000000 + 100000000 + order.index(second_pair.value)*1000000 + 1000000 + order.index(temp_hand2[0].value)*10000 + 10000
    else:
        #last card should be highest, because temp_hand is sorted
        return 10000000000 + order.index(temp_hand[4].value)*100000000 + 100000000 + order.index(temp_hand[3].value)*1000000 + 1000000 + order.index(temp_hand[2].value)*10000 + 10000 + order.index(temp_hand[1].value)*100 + 100 + order.index(temp_hand[0].value)*1 + 1


def highest_combination(hand, num=5):
    '''Returns the highest scoring num-Card combination of a given hand.'''
    current_highest = 0
    highest_hand = []
    from itertools import combinations
    for hand_combo in combinations(hand, num):
        if hand_score(list(hand_combo)) > current_highest:
            current_highest = hand_score(list(hand_combo))
            highest_hand = list(hand_combo)
    highest_hand.sort()
    return highest_hand

def generate(num=5):
    '''Randomly generates a num-carded hand, from a standard Deck of 52 Cards.'''
    deck = Deck()
    deck.new_deck_value()
    deck.shuffle()
    return [deck.container[i] for i in range(num)]
    

if __name__ == '__main__':
    d = Deck()
    d.new_deck_value()
    d.shuffle()
    hand = [Card(5,'d'), Card('Q','d'), Card('K','d'), Card(7,'s'), Card(6,'d')]
    print(hand)
    print(hand_score(hand))
    hand = [Card(5,'d'), Card('Q','d'), Card('K','d'), Card(6,'s'), Card(6,'d')]
    print(hand)
    print(hand_score(hand))
    hand = [Card(5,'d'), Card('K','s'), Card('K','d'), Card(6,'s'), Card(6,'d')]
    print(hand)
    print(hand_score(hand))
    hand = [Card(5,'d'), Card('Q','d'), Card(6,'c'), Card(6,'s'), Card(6,'d')]
    print(hand)
    print(hand_score(hand))
    hand = [Card(5,'d'), Card(8,'d'), Card(9,'d'), Card(6,'s'), Card(7,'d')]
    print(hand)
    print(hand_score(hand))
    hand = [Card(5,'d'), Card('Q','d'), Card('K','d'), Card(7,'d'), Card(6,'d')]
    print(hand)
    print(hand_score(hand))
    hand = [Card('Q','c'), Card('Q','d'), Card(6,'c'), Card(6,'s'), Card(6,'d')]
    print(hand)
    print(hand_score(hand))
    hand = [Card(10,'c'), Card(10,'d'), Card(10,'h'), Card(10,'s'), Card(4,'d')]
    print(hand)
    print(hand_score(hand))
    hand = [Card(5,'d'), Card(8,'d'), Card(9,'d'), Card(6,'d'), Card(7,'d')]
    print(hand)
    print(hand_score(hand))
