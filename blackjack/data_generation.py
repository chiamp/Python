import numpy as np
from deck import *
from game import *

PLAYER_WIN = 'player_win'
DEALER_WIN = 'dealer_win'
TIE = 'tie'

PLAYER = 'player'
DEALER = 'dealer'

HIT = 'hit'
STAY = 'stay'
DD = 'double_down'
SPLIT = 'split'

def softmax(x,base=np.e):
    #experiment with different bases?
    return (base**(x))/np.sum(base**(x))

def get_truth(array):
    #takes the array returns and flattens them so only the maximum returns remain
    #e.g. get_truth([1,0,2,-1]) --> [0,0,1,0]
    #if there is a tie, distribute the points evenly so that they add up to 1
    maximum = -np.inf
    num_max = 0
    for num in array:
        if num == maximum:
            num_max += 1
            maximum = num
        elif num > maximum:
            maximum = num
            num_max = 1
    return np.array([0 if array[i]!=maximum else 1/num_max for i in range(4)])

def simulate_round(g):
    #data = []
    feature_list = [g.get_features()]
    output_list = np.array([0,0,0,-np.inf]) #[HIT,STAY,DD,SPLIT]
    #output_list represents returns for each play (Assume typical bet is value 1)
    #Typically, +1 for win, -1 for lose, 0 for tie
    #+2 if you win for DD, -2 if you lose for DD
    #take the max to get the highest return; this will be treated as the "correct"/"optimal" play and will serve as the basis of the ground truth vector

    #HIT
    g_copy = g.copy()
    ##print('hit')
    output_list[0],hit_data,hit_truth = simulate_hit(g_copy)
    ##print(g_copy)
    ##print('return: {}'.format(output_list[0]))
    ##print('hit_data: {}'.format(hit_data))
    ##print()

    #STAY
    g_copy = g.copy()
    ##print('stay')
    output_list[1] = simulate_stay(g_copy)
    ##print(g_copy)
    ##print('return: {}'.format(output_list[1]))
    ##print()

    #DD
    g_copy = g.copy()
    ##print('double down')
    output_list[2] = simulate_dd(g_copy)
    ##print(g_copy)
    ##print('return: {}'.format(output_list[2]))
    ##print()

    #SPLIT
    #negative infinity so that if we softmax, the probability to do the split action is 0
    #this is in the case that split is not a legal option in the game
    g_copy = g.copy()
    split_data = None
    if len(g.player.hand.hand) == 2 and g.player.hand.hand[0] == g.player.hand.hand[1]:
        ##print('split')
        output_list[3],split_data,split_truth = simulate_split(g_copy)
        ##print(g_copy)
        ##print('return: {}'.format(output_list[3]))
        ##print('split_data: {}'.format(split_data))
        ##print()

    #flatten so that only max returns remain
    truth_vector = [get_truth(output_list)]
##    data.append([feature_list,truth_vector]) #append to input and expected output (as ground truth) to data
##    data += hit_data #add the additional data from the recursive calls of simulate_hit()
##    if split_data != None:
##        data += split_data
    if hit_data != None:
        feature_list += hit_data
        truth_vector += hit_truth
    if split_data != None:
        feature_list += split_data
        truth_vector += split_truth
    return feature_list,truth_vector

def simulate_hit(g):
    data = [] #format [[feature_list1,prob1],[feature_list2,prob2],...,[feature_listN,probN]]
    g.hit(PLAYER)
    if g.player.get_low_hand_value() > 21 or (g.player.get_high_hand_value() > 21 and g.player.get_low_hand_value() == 0):
        #player busts and loses
        return -1,data,[]
    elif g.player.get_low_hand_value == 21 or g.player.get_high_hand_value == 21:
        g.dealer_move()
        result = g.evaluate()
        #there's no way dealer can win if player has a hand value of 21
        if result == PLAYER_WIN:
            return 1,data,[]
        else:
            #TIE
            return 0,data,[]
    else:
        #recursively try out every action given our new game state and its features
        feature_list = [g.get_features()]
        output_list = np.array([0,0,0,-np.inf]) #[HIT,STAY,DD,SPLIT]

        #HIT
        g_copy = g.copy()
        ##print('hit')
        output_list[0],hit_data,hit_truth = simulate_hit(g_copy)
        ##print(g_copy)
        ##print('return: {}'.format(output_list[0]))
        ##print('hit_data: {}'.format(hit_data))
        ##print()

        #STAY
        g_copy = g.copy()
        ##print('stay')
        output_list[1] = simulate_stay(g_copy)
        ##print(g_copy)
        ##print('return: {}'.format(output_list[1]))
        ##print()

        #DD
        g_copy = g.copy()
        ##print('double down')
        output_list[2] = simulate_dd(g_copy)
        ##print(g_copy)
        ##print('return: {}'.format(output_list[2]))
        ##print()

        #SPLIT
        #negative infinity so that if we softmax, the probability to do the split action is 0
        #this is in the case that split is not a legal option in the game
        split_data = None
        g_copy = g.copy()
        if len(g.player.hand.hand) == 2 and g.player.hand.hand[0] == g.player.hand.hand[1]:
            ##print('split')
            output_list[3],split_data,split_truth = simulate_split(g_copy)
            ##print(g_copy)
            ##print('return: {}'.format(output_list[3]))
            ##print('split_data: {}'.format(split_data))
            ##print()

        #flatten so that only max returns remain
        truth_vector = [get_truth(output_list)]
##        data.append([feature_list,truth_vector]) #append to input and expected output (as ground truth) to data
##        data += hit_data #add the additional data from the recursive calls of simulate_hit()
##        if split_data != None:
##            data += split_data #add the additional data from the recursive calls of simulate_split()
        if hit_data != None:
            feature_list += hit_data
            truth_vector += hit_truth
        if split_data != None:
            feature_list += split_data
            truth_vector += split_truth
        
        #return the maximum return
        return max(output_list),feature_list,truth_vector

def simulate_stay(g):
    g.dealer_move()
    result = g.evaluate()
    if result == PLAYER_WIN:
        return 1
    elif result == DEALER_WIN:
        return -1
    else:
        return 0

def simulate_dd(g):
    g.double_down()
    if g.player.get_low_hand_value() > 21 or (g.player.get_high_hand_value() > 21 and g.player.get_low_hand_value() == 0):
        #player busts and loses
        return -2
    else:
        g.dealer_move()
        result = g.evaluate()
        if result == PLAYER_WIN:
            return 2
        elif result == DEALER_WIN:
            return -2
        else:
            return 0

def simulate_split(g):
    g1 = g.copy()
    g1.player.hand.hand.pop(0)
    g2 = g.copy()
    g2.player.hand.hand.pop(1)
    #split to Games g1 and g2 with one card in hand each
    #then hit both, so they both have two cards in hand
    return1,split_data1,truth_vector1 = simulate_hit(g1)
    return2,split_data2,truth_vector2 = simulate_hit(g2)
    total_return = return1 + return2
    split_data = split_data1 + split_data2
    truth_vector = truth_vector1 + truth_vector2
    return total_return,split_data,truth_vector


def convert(array_list):
    #print the hand values given the input feature vector array_list
    for lst in array_list:
        print(get_hand_value(lst[0][10:13]),get_hand_value(lst[0][13:]),lst[1]) #player_hand, dealer_hand, probabilities for HIT,STAY,DD,SPLIT

def get_hand_value(lst):
    return_list = []
    return_list.append('hand_values: [{},{}]'.format(lst[0]*21,lst[1]*21))
    if len(lst) == 3:
        return_list.append('can_split: {}'.format(lst[2]))
    return return_list


def get_all_player_hands():
    #generate all possible player hands
    hand_list = [Hand([Card('A'),Card('A')])]
    for i in range(2,10+1):
        #add all two-card hand combinations that contain an Ace
        hand_list.append(Hand([Card('A'),Card(str(i))]))
    for i in range(2,10+1):
        #add all possible split hand combinations
        hand_list.append(Hand([Card(str(i)),Card(str(i))]))
    for i in range(5,19+1):
        #hand values 2 to 4 were already made in the previous for loops
        if i%2 == 1:
            hand_list.append(Hand([Card(str(int(i//2))),Card(str(int(i//2)+1))]))
        else:
            #to prevent getting split combinations
            hand_list.append(Hand([Card(str(int(i//2-1))),Card(str(int(i//2)+1))]))
    #it's impossible to create a non-splitting hand with a value of 21 or 20 with only two-card combinations, without using an Ace
    hand_list.append(Hand([Card('8'),Card('7'),Card('5')]))
    hand_list.append(Hand([Card('8'),Card('7'),Card('6')]))
    return hand_list #size 36

def get_all_dealer_hands():
    #generate all possible dealer hands
    #need all combinations because we treat the 0th index card as the hidden card
    card_list = ['A','2','3','4','5','6','7','8','9','10']
    hand_list = []
    for i in range(len(card_list)):
        for j in range(len(card_list)):
            hand_list.append(Hand([Card(card_list[i]),Card(card_list[j])]))
    return hand_list #size 100


def simulate_rounds(deck,deck_size,player,dealer,n=1):
    #data = []
    player_hand_list = get_all_player_hands()
    dealer_hand_list = get_all_dealer_hands()
    g = Game(player,dealer,deck)

    feature_list = []
    truth_vector = []

    i=1
    for _ in range(n):
        for player_hand in player_hand_list:
            #print(i)
            for dealer_hand in dealer_hand_list:
                g.new_deck(deck_size)
                g.player.set_hand(player_hand)
                g.dealer.set_hand(dealer_hand)
                features,truths = simulate_round(g)
                feature_list += features
                truth_vector += truths
            i+=1
    return feature_list,truth_vector


if __name__ == '__main__':
    d = Deck()
    player = Player('Bob')
    dealer = Dealer()
    g = Game(player,dealer,d)

    #data = simulate_rounds(deck,52,player,dealer,n=2)

    d.deck = [Card('A'),Card('5'),Card('2'),Card('Q'),Card('10'),Card('A'),Card('5'),Card('2'),Card('J'),Card('K')]
    player.hand.hand = [Card('7'),Card('7')]
    dealer.hand.hand = [Card('8'),Card('7')]
    feature_list,truth_vector = simulate_round(g)
    
    
