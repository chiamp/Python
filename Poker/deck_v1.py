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
    @rtype: list[int, Card] | formatted as [points, highest card in hand]
    
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
    '''
    assert len(hand) == 5
    order = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
    temp_hand = hand[:]
    temp_hand.sort() #sorted from lowest to highest
    if order.index(temp_hand[4].value) - order.index(temp_hand[3].value) == 1 and order.index(temp_hand[3].value) - order.index(temp_hand[2].value) == 1 and order.index(temp_hand[2].value) - order.index(temp_hand[1].value) == 1 and order.index(temp_hand[1].value) - order.index(temp_hand[0].value) == 1:
        if temp_hand[4].suit == temp_hand[3].suit == temp_hand[2].suit == temp_hand[1].suit == temp_hand[0].suit:
            return [9, temp_hand[4]]
        else:
            return [5, temp_hand[4]]
    if temp_hand[4].suit == temp_hand[3].suit == temp_hand[2].suit == temp_hand[1].suit == temp_hand[0].suit: #all suits same, but not in order
        return [6, temp_hand[4]]

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
        return [8, max_counter[1]]
    if max_counter[0] == 3:
        if len(multiple_dict) == 2: #meaning there are only two entries for the card.value keys; meaning that if one of them is length 3, the other one must be length 2
            return [7, max_counter[1]]
        else:
            return [4, max_counter[1]]
    if max_counter[0] == 2:
        if len(multiple_dict) == 4: #meaning it's only a one pair
            return [2, max_counter[1]]
        else: #meaning there is two pair
            highest_value = Card(2, 'D') #lowest card possible
            for key in multiple_dict:
                if len(multiple_dict[key]) == 2:
                    if multiple_dict[key][0] > highest_value:
                        highest_value = multiple_dict[key][0]
            return [3, highest_value]
    else:
        return [1, temp_hand[-1]] #last card should be highest, because temp_hand is sorted

def compare_hand(hand1, hand2):
    '''Returns the hand with higher value. Returns 0 if both hands are equal (meaning they tie).
    @type hand1: list[Card]
    @type hand2: list[Card]
    @rtype: list[Card]
    '''
    if len(hand1) == 5 and len(hand2) == 5:
        score1, score2 = hand_score(hand1), hand_score(hand2)
        if score1[0] > score2[0]:
            return hand1
        if score2[0] > score1[0]:
            return hand2
        if score1[1] > score2[1]:
            return hand1
        if score2[1] > score1[1]:
            return hand2
        else: #they are both equal in score and highest card in hand
            multiple_dict1 = {} #{card.value: list[Card]}
            for card in hand1:
                if card.value not in multiple_dict1:
                    multiple_dict1[card.value] = [card]
                else:
                    multiple_dict1[card.value].append(card)
            multiple_dict2 = {} #{card.value: list[Card]}
            for card in hand1:
                if card.value not in multiple_dict1:
                    multiple_dict2[card.value] = [card]
                else:
                    multiple_dict2[card.value].append(card)

            if score1 == 8: #four of a kind
                for key in multiple_dict1:
                    if len(multiple_dict1[key]) == 1:
                        kicker1 = multiple_dict1[key][0]
                for key in multiple_dict2:
                    if len(multiple_dict2[key]) == 1:
                        kicker2 = multiple_dict2[key][0]
                if kicker1 > kicker2:
                    return hand1
                if kicker2 > kicker1:
                    return hand2
                else: #both kickers are equal, meaning whole hand is equal, meaning tie
                    return 0
            if score1 == 7:
                for key in multiple_dict1:
                    if len(multiple_dict1[key]) == 2:
                        kicker1 = multiple_dict1[key][0]
                for key in multiple_dict2:
                    if len(multiple_dict2[key]) == 2:
                        kicker2 = multiple_dict2[key][0]
                if kicker1 > kicker2:
                    return hand1
                if kicker2 > kicker1:
                    return hand2
                else: #both kickers are equal, meaning whole hand is equal, meaning tie
                    return 0
            if score1 == 6:
                
    else: #recursion
        if 


def kicker_score(hand, score):
    '''Returns kicker score.
    @type hand: list[Card]
    @type score: int (range 1 to 9 inclusive)
    @rtype: float

    Kicker score rankings:
    A - 0.13
    K - 0.12
    Q - 0.11
    J - 0.10
    10 - 0.09
    9 - 0.08
    8 - 0.07
    7 - 0.06
    6 - 0.05
    5 - 0.04
    4 - 0.03
    3 - 0.02
    2 - 0.01
    '''
    kicker_ranking = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
    temp_hand = hand[:]
    temp_hand.sort() #sorted from lowest to highest
    
    multiple_dict = {} #{card.value: list[Card]}
    for card in temp_hand:
        if card.value not in multiple_dict:
            multiple_dict[card.value] = [card]
        else:
            multiple_dict[card.value].append(card)
            
    if score == 8: #four of a kind
        for key in multiple_dict:
            if len(multiple_dict[key]) == 1:
                return 0.01*(kicker_ranking.index(multiple_dict[key][0]) + 1)
    if score == 7: #full house
        for key in multiple_dict:
            if len(multiple_dict[key]) == 2:
                return 0.01*(kicker_ranking.index(multiple_dict[key][0]) + 1)
    if score == 4: #three of a kind
        

if __name__ == '__main__':
    d = Deck()
    d.new_deck_value()
    d.shuffle()
    hand = [Card('J','d'), Card('A','d'), Card(10,'c'), Card(4,'h'), Card(2,'s')]
