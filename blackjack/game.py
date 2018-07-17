from deck import *
import numpy as np
from neural_network import *
import torch

PLAYER_WIN = 'player_win'
DEALER_WIN = 'dealer_win'
TIE = 'tie'

PLAYER = 'player'
DEALER = 'dealer'

HIT = 'hit'
STAY = 'stay'
DD = 'double_down'
SPLIT = 'split'

class Player:
    def __init__(self,name='Test',money=1000):
        self.hand = Hand([])
        self.name = name
        self.money = money
        self.a_card = Card('A')
    def clear_hand(self):
        self.hand = Hand([])
    def set_hand(self,hand):
        self.hand = hand
    def add_card(self,card):
        self.hand.add_card(card)
    def get_high_hand_value(self):
        return self.hand.get_high_value()
    def get_low_hand_value(self):
        #return 0 if no Aces are in the hand
        return self.hand.get_low_value()
    def can_split(self):
        #return 1 if you can split, otherwise 0
        if len(self.hand.hand) == 2 and self.hand.hand[0] == self.hand.hand[1]:
            return 1
        else:
            return 0
    def get_features(self):
        #[high_hand_value,low_hand_value,can_split]
        #normalize hand values to be out of 21
        return [self.get_high_hand_value()/21,self.get_low_hand_value()/21,self.can_split()] #size 3
    def copy(self):
        p_copy = Player(self.name,self.money)
        p_copy.hand = self.hand.copy()
        return p_copy
    def __str__(self):
        return '{} (${}): {}'.format(self.name,self.money,self.hand)
    def __repr__(self):
        return str(self)

class Dealer(Player):
    def __init__(self):
        Player.__init__(self,'Dealer')
    def copy(self):
        d_copy = Dealer()
        d_copy.hand = self.hand.copy()
        return d_copy
    def get_partial_high_hand_value(self):
        #partial hand value ignores hidden card (for the purpose of calculating dealer features)
        temp_hand = self.hand.copy()
        temp_hand.hand = temp_hand.hand[1:] #subset to ignore the 0th index, as that is the hidden card
        return temp_hand.get_high_value()
    def get_partial_low_hand_value(self):
        #partial hand value ignores hidden card (for the purpose of calculating dealer features)
        temp_hand = self.hand.copy()
        temp_hand.hand = temp_hand.hand[1:] #subset to ignore the 0th index, as that is the hidden card
        return temp_hand.get_low_value()
    def get_features(self):
        #[high_hand_value,low_hand_value]
        #treat 0th index as the hidden card and 1st index as the revealed card
        return [self.get_partial_high_hand_value()/21,self.get_partial_low_hand_value()/21] #size 2
    def __str__(self):
        return '{}: {}'.format(self.name,self.hand)
    def __repr__(self):
        return str(self)    

class Game:
    def __init__(self,player,dealer,deck):
        self.player = player
        self.player_bet = 0
        self.dealer = dealer
        self.deck = deck
    def evaluate(self):
        #if self.player.get_high_hand_value() > 21 and self.dealer.get_high_hand_value() > 21:
        #    return -1
        if self.player.get_high_hand_value() > 21:
            return DEALER_WIN
        elif self.dealer.get_high_hand_value() > 21:
            return PLAYER_WIN
        elif self.player.get_high_hand_value() > self.dealer.get_high_hand_value():
            return PLAYER_WIN
        elif self.player.get_high_hand_value() < self.dealer.get_high_hand_value():
            return DEALER_WIN
        else:
            return TIE
    def move_pot(self,status,pot=None):
        #pot != None when we are under split
        if status == PLAYER_WIN:
            if pot == None:
                self.player.money += self.player_bet*2
            else:
                self.player.money += pot*2
        elif status == TIE:
            if pot == None:
                self.player.money += self.player_bet
            else:
                self.player.money += pot
        self.player_bet = 0 #empty the pot regardless
    def bet(self,money=10):
        self.player_bet += money
        self.player.money -= money
    def hit(self,person):
        if person == PLAYER:
            self.player.add_card(self.deck.draw_top_card())
        elif person == DEALER:
            self.dealer.add_card(self.deck.draw_top_card())
    def double_down(self,pot=None):
        self.hit(PLAYER)
        if pot == None:
            self.player.money -= self.player_bet
            self.player_bet *= 2
        else:
            #in the case of split, don't affect the actually player_bet
            #but keep track of how much you bet in total
            self.player.money -= pot
    def dealer_move(self):
        while self.dealer.get_high_hand_value() < 17: #dealer will stay on a soft 17
            self.hit(DEALER)
    def new_deck(self,deck_size):
        self.deck.initiate_deck_size(deck_size)
    def begin_round(self,bet=10):
        self.player.clear_hand()
        self.dealer.clear_hand()
        self.bet(bet)
        self.hit(PLAYER)
        self.hit(PLAYER)
        self.hit(DEALER)
        self.hit(DEALER)
    def play_game(self,ai=False,depth=20):
        while True:
            #when there are depth cards or less remaining in the deck, restart to 52
            if len(self.deck.deck) <= depth:
                self.new_deck(52)
            self.begin_round()
            print(str(self)+'\n')
            self.execute_player_move(ai)
    def execute_player_move(self,ai=False,pot=None):
        if ai == True:
            move = self.player.get_move(self.get_features()) #AI class method
        else:
            move = input('Input move: ')
        print('Player {}'.format(move))
        if move == 'HIT':
            self.hit(PLAYER)
            print(str(self)+'\n')
            #if high hand value is greater than 21, check the low hand value
            #if it's also greater than 21, then it is a bust
            #if the low hand value is a 0, that means no Ace exists in the hand and it is also a bust
            if self.player.get_high_hand_value() > 21 and (self.player.get_low_hand_value() > 21 or self.player.get_low_hand_value() == 0):
                status = self.evaluate()
                print(status+'\n')
                self.move_pot(status,pot)
            else:
                self.execute_player_move(ai)
        elif move == 'STAY':
            self.dealer_move()
            print(str(self)+'\n')
            status = self.evaluate()
            print(status+'\n')
            self.move_pot(status,pot)
        elif move == 'DD':
            self.double_down(pot)
            self.dealer_move()
            print(str(self)+'\n')
            status = self.evaluate()
            print(status+'\n')
            self.move_pot(status,pot)
        else:
            #bet additional money for splitting for each hand
            self.player.money -= self.player_bet
            #keep track of how much was in the pot before splitting
            pot = self.player_bet
            card = self.player.hand.hand[0]
            dealer_hand = self.dealer.hand.copy()
            for _ in range(2):
                self.player_bet = pot
                self.player.hand.hand = [card]
                self.dealer.hand = dealer_hand.copy()
                self.hit(PLAYER)
                print(str(self)+'\n')
                self.execute_player_move(ai,pot)
    def get_features(self):
        feature_list = self.deck.get_features() #size 10, contains counts of cards, not probabilities
        #increase count by 1 for probability of drawing that hidden card, since the information on the hidden card is not known to the player
        if self.dealer.hand.hand[0] == self.dealer.a_card:
            feature_list[9] += 1
        else:
            feature_list[self.dealer.hand.hand[0].high_value-2] += 1
        feature_list = [i/(len(self.deck.deck)+1) for i in feature_list] #treat the deck having one more card (factoring the hidden card)
        feature_list += self.player.get_features() #size 3
        feature_list += self.dealer.get_features() #size 2
        #concatenate deck, player and dealer features
        return np.array(feature_list,dtype='float32') #size 15; float32 dtype necessary for neural network
    def copy(self):
        #create completely new instance
        return Game(self.player.copy(),self.dealer.copy(),self.deck.copy())
    def __str__(self):
        return '{}\n{}\n{}\nPot: {}'.format(str(self.deck),str(self.player),str(self.dealer),str(self.player_bet))
    def __repr__(self):
        return str(self)

class AI(Player):
    def __init__(self,filename=None):
        Player.__init__(self,'AI')
        self.net = Net()
        if filename != None:
            self.load_weights(filename)
    def load_weights(self,filename):
        self.net.load_state_dict(torch.load('weights\\'+filename+'.pt'))
    def get_move(self,game_features):
        #get highest percentage move
        index = int(torch.argmax(self.net(torch.from_numpy(game_features).view(1,15))))
        return ['HIT','STAY','DD','SPLIT'][index]

if __name__ == '__main__':
    d = Deck()
    d.initiate_standard_deck()
    #d.initiate_deck_size(30)
    #d.deck = [Card('3') for _ in range(52)]
    #p = Player('Bob')
    p = AI('2_layers')
    de = Dealer()
    g = Game(p,de,d)
    g.play_game(ai=True)

