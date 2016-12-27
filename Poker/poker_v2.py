from deck_v2 import *

class Poker:
    '''Poker class for the game'''
    def __init__(self, player_list=[], string=True):
        '''Initializes the Poker class.
        @type self: Poker
        @type player_list: list[Player]
        @type deck: Deck
        @type self.turn: Player
        @type self.pot: float
        @type self.board: list[Card]
        '''
        self.player_list = player_list #Player at index 0 is the active Player
        self.string = string #this parameter is just for the string method recursion; it is only True when it is the first instance; all subsequent recursion levels are False
        
        self.deck = Deck()
        self.deck.new_deck_suit()
        self.deck.shuffle()
        #self.turn = turn

        self.round = 1 #keeps track of the number of rounds
        self.big_blind = None
        self.small_blind = None
        self.min_bet = None
        
        self.board = []
        self.current_players = [] #current Players in the round that have not folded
        self.pot = 0
        self.bet_tracker = {} #keeps track of how much each Player has bet during the round; format: dict{Player:[money bet, all-in bool]}
        self.discard = [] #for Cards of Players that have folded
    def __str__(self):
        assert len(self.player_list) >= 1
        if len(self.player_list) == 1:
            return self.player_list[0].__str__()
        if self.string == True:
            return 'Board: {}\nPot: ${}\n'.format(self.board, self.pot) + '{}\n'.format(self.player_list[0]) + '{}'.format(Poker(self.player_list[1:], False).__str__())
        else:
            return '{}\n'.format(self.player_list[0]) + '{}'.format(Poker(self.player_list[1:], False).__str__())
    def __repr__(self):
        return 'Poker({})'.format(self.player_list)
    def add_players(self, lst):
        '''Add Players to self.player_list.'''
        for player in lst:
            self.player_list.append(player)
    def all_reveal(self):
        '''Makes all Players in self.current_players reveal their hands'''
        for player in self.current_players:
            player.reveal_hand()
    def all_hide(self):
        '''Makes all Players in self.current_players hide their hands'''
        for player in self.current_players:
            player.hide_hand()
    def game_start(self, big_blind, small_blind=None, min_bet=None, money=0):
        assert len(self.player_list) > 1
        for player in self.player_list:
            player.money += money #give each Player money
            self.bet_tracker[player] = [0, False] #create a key in the self.bet_tracker dictionary for each player; format: dict{Player:[money bet, all-in bool]}

        self.big_blind = big_blind #determine the value of blinds and minimum bet
        if small_blind == None:
            self.small_blind = big_blind/2
        if min_bet == None:
            self.min_bet = big_blind
        self.player_list[-1].bb() #making big blind last means that the first Player to bet will be the one at index 0 in self.player_list / self.current_players
        self.player_list[-2].sb()
    def deal(self):
        print('-ROUND {}-\nDealing...'.format(self.round))
        for player in self.player_list:
            player.hand.append(self.deck.pop_left())
            player.hand.append(self.deck.pop_left())
            self.current_players.append(player) #all Players are now added to the list self.current_players
    def ante_up(self):
        '''All Players with blinds put money into the pot.
        If a Player does not have enough to meet blind requirements, he goes all in.'''
        for player in self.current_players:
            if player.blind == 'b':
                if player.money >= self.big_blind:
                    player.ante(self.big_blind)
                    self.pot += self.big_blind
                    self.bet_tracker[player][0] += self.big_blind
                    print('{} is big blind. Puts ${} into the pot.'.format(player.name, self.big_blind))
                else: #not enough money for big blind
                    print('{} is big blind. Puts ${} into the pot. {} is all in.'.format(player.name, player.money, player.name))
                    self.pot += player.money
                    self.bet_tracker[player][0] += player.money
                    self.bet_tracker[player][1] = True #player is all in
                    player.ante(player.money) #bet all his money
            elif player.blind == 's':
                if player.money >= self.small_blind:
                    player.ante(self.small_blind)
                    self.pot += self.small_blind
                    self.bet_tracker[player][0] += self.small_blind
                    print('{} is small blind. Puts ${} into the pot.'.format(player.name, self.small_blind))
                else: #not enough money for small blind
                    print('{} is small blind. Puts ${} into the pot. {} is all in.'.format(player.name, player.money, player.name))
                    self.pot += player.money
                    self.bet_tracker[player][0] += player.money
                    self.bet_tracker[player][1] = True #player is all in
                    player.ante(player.money) #bet all his money
    def check_high_bet(self):
        '''Checks the highest bet to match, in the dictionary self.bet_tracker'''
        highest_bet = 0
        for player in self.bet_tracker:
            if self.bet_tracker[player][0] > highest_bet:
                highest_bet = self.bet_tracker[player][0]
        return highest_bet
    def betting_round(self):
        bet_equal = False #only True when every player in self.current_players has bet the same amount (unless a Player is all in)
        counter = 0 #Player turn index
        while bet_equal == False:
            betting_player = self.current_players[0]
            print('Bet to match: ${}'.format(self.check_high_bet()))
            print("{}'s current bet: ${}".format(self.bet_tracker[betting_player][0]))
            print('Minimum bet: ${}'.format(self.min_bet))
            bet_prompt(betting_player)
            counter += 1

            total = 0 #divide this by number of non-all in Players and see if it is the same as the check value
            check = 0
            num_nai_players = 0 #number of Not All In players
            for player in self.current_players:
                if self.bet_tracker[player][1] == False: #meaning that specific player is not all in
                    total += self.bet_tracker[player][0] #add their total bet into the total
                    check = self.bet_tracker[player][0] #this will repeat and overwrite a number of times, but theoretically if all bets are the same (minus all in Players), the check value should be the same thing everytime
                    num_nai_players += 1
            if total / num_nai_players == check:
                bet_equal = True
        print('This round of betting has concluded. Pot contains ${}.'.format(self.pot))
    def bet_prompt(self, player):
        '''Helper function for betting_round method. Prompts the current betting_player for a move in {'check', 'call', 'raise', 'fold'}
        and alters the player.money, self.bet_tracker[player] and self.pot accordingly.'''
        move = input('{} to move. '.format(player.name))
        while move.lower() not in {'c', 'check', 'call', 'r', 'raise', 'f', 'fold'}:
            move = input("Invalid input. Please type 'c' for check/call, 'r' for raise, or 'f' for fold. ")
        if move in {'c', 'check', 'call'}:
            if self.bet_tracker[player][1] == False: #which means he is not all in
                bet = self.check_high_bet() - self.bet_tracker[player][0]
                player.money -= bet
                self.bet_tracker[player][0] += bet
                self.pot += bet
                print('{} checks/calls. ${} added to the pot.'.format(player.name, bet))
            else: #if he is all in, no need to do anything; player.money remains 0, self.bet_tracker[player][0] remains the same, self.pot remains the same
                print('{} forced to check because he is all in.'.format(player.name))
        if move in {'f', 'fold'}:
            self.current_players.remove(player)
            #self.bet_tracker[player][0] = 0 ; if another Player is all in and wins, this current Player should get part of his money back if the all in Player couldn't reach max bet
            self.discard.append(player.hand.pop()) #put 1st folded card into self.discard
            self.discard.append(player.hand.pop()) #put 2nd folded card into self.discard
            print('{} folds.'.format(player.name))
            assert len(player.hand) == 0
        else: #raise
            #move should be in format 'r bet_money' or 'raise bet_money'
            move = move.split() #0 index is 'r' or 'raise', 1 index is money
            assert len(move) == 2
            bet_money = int(move[1])
            if bet_money < self.min_bet or bet_money > player.money:
                bet_money = int(input('Minimum bet is ${}. Please bet a number equal to that or higher. You cannot bet more than what you have. Current money: ${}. '.format(self.min_bet, player.money)))
            player.money -= bet_money
            self.bet_tracker[player][0] += bet_money
            self.pot += bet_money
            print('{} raises with a bet of ${}.'.format(player.name, bet_money))
    def check_players(self):
        '''Checks to see if there is only one remaining Player left.'''
        return len(self.current_players) == 1
    
    def the_flop(self):
        print('The Flop.')
        self.board.append(self.deck.pop_left())
        self.board.append(self.deck.pop_left())
        self.board.append(self.deck.pop_left())
        print(self)
        self.betting_round()
    def the_turn(self):
        print('The Turn.')
        self.board.append(self.deck.pop_left())
        print(self)
        self.betting_round()
    def the_river(self):
        print('The River.')
        self.board.append(self.deck.pop_left())
        self.all_reveal() #All Players reveal their hands after the River.
        print(self)
        highest_scoring = [0, [], None] #[hand_score, highest_hand, Player]
        ties = {} #dict{score:dict{Player:[hand]}}
        for player in self.current_players:
            highest_hand = highest_combination(player.hand + self.board)
            if hand_score(highest_hand) > highest_scoring[0]:
                highest_scoring = [hand_score(highest_hand), highest_hand, player]
            elif hand_score(highest_hand) == highest_scoring[0]: #tie
                ties[hand_score(highest_hand)] = {player: highest_hand} #for current Player
                ties[highest_scoring[0]][highest_scoring[2]] = highest_scoring[1] #for top Player; #hand_score(highest_hand) should == highest_scoring[0], so the key should already exist
        if ties == {}: #no ties
            winner = highest_scoring[2]
            winning_hand = highest_scoring[1]
            if self.bet_tracker[winner][1] == False: #meaning he did not go all in
                print('{} wins the ${} pot with a hand of {}.'.format(winner.name, self.pot, winning_hand))
                winner.money += self.pot
                self.pot = 0
            else: #he did go all in
                bet_amount = self.bet_tracker.pop(winner)[0] #we only want the 0 index as the 1 index just points to a bool
                self.current_players.remove(winner)
                #the winning player has been taken out of self.bet_tracker and self.current_players
                print('{} wins with a hand of {}.'.format(winner.name, winning_hand))
                print('Players may receive a portion of their bet back, because {} went all in.'.format(winner.name))
                total_gained = 0
                for player in self.bet_tracker:
                    if self.bet_tracker[player][0] >= bet_amount: #if this Player has bet more or equal to the winning Player's bet amount
                        total_gained += bet_amount
                        print('{} receives ${} back from the pot.'.format(player.name, self.bet_tracker[player][0] - bet_amount))
                        player.money += self.bet_tracker[player][0] - bet_amount #add the remaining difference back to the Player's money
                        self.pot -= self.bet_tracker[player][0] #unnecessary line
                    else: #the player bet less than the winning Player's bet amount
                        total_gained += self.bet_tracker[player][0] #add all of it
                        print('{} receives $0 back from the pot.'.format(player.name))
                        self.pot -= self.bet_tracker[player][0]
                assert self.pot == 0
                print('{} wins ${} from the pot.'.format(winner.name, total_gained))
        else: #there is a tie
            top_score = 0
            for score in ties:
                if score > top_score:
                    top_score = score
            #at this point, we should have the top score out of all hands
            winner_list = [] #format: list[list[Player, hand, bet_money]]
            for player in ties[top_score]:
                winner_list.append([player, ties[top_score][player], self.bet_tracker[player][0]])
            sorted_winner_list = [] #same format as winner_list
            for lst in winner_list: #sorting from lowest to highest according to the amount they bet
                if sorted_winner_list == []:
                    sorted_winner_list.append(lst)
                else:
                    counter = 0
                    while counter < len(sorted_winner_list) and sorted_winner_list[counter][2] < lst[2]: #if the bet_money is smaller than current bet_money
                        counter += 1
                    sorted_winner_list.insert(counter, lst)
            for player in self.bet_tracker:
                if sorted_winner_list[-1][2] < self.bet_tracker[player][0]: #if this Player bet more than the winning Player with the highest amount of bet money among the tie winners
                    player.money += self.bet_tracker[player][0] - sorted_winner_list[-1][2] #return the difference in bet money to that Player
                    self.pot -= self.bet_tracker[player][0] - sorted_winner_list[-1][2]
            #self.pot should have all money that can be distributed now
            cumulative_gain = 0 #to keep track of money thats to be added upon for winners who bet more than others
            num_distribution = len(winner_list) #keep track of how many people get money from this specific sub-pot
            for i in range(len(winner_list)-1):
                gain_money = (winner_list[i+1][2] - winner_list[i][2]) #gain_money is how much money each Player gets
                index = len(winner_list) - num_distribution
                if gain_money != 0:
                    for x in range(num_distribution):
                        sorted_winner_list[index][0].money += gain_money

    def check_losers(self):
        for player in self.player_list:
            if player.money <= 0: #if a player has $0, they lose the game
                self.player_list.remove(player)
                print('{} has lost the game.'.format(player.name))
    def cleanup(self):
        for player in self.current_players:
            self.deck.append(player.hand.pop())
            self.deck.append(player.hand.pop())
        print("All players' cards returned to deck.")
        for _ in range(len(self.board)):
            self.deck.append(self.board.pop())
        print('All cards on the board returned to deck.')
        for _ in range(len(self.discard)):
            self.deck.append(self.discard.pop())
        print('All discarded cards returned to deck.')
        print('Shuffling deck...')
        assert len(self.deck) == 52
        self.deck.shuffle()
        self.current_players = []
        self.round += 1
    def next_blind(self):
        '''Moves the active Player (Player at index 0 of self.player_list) to the back of the list.
        The new Player occupying index 0 has the active turn now.
        Assign new players big and small blind status.
        '''
        insert_player = self.player_list.pop(0)
        self.player_list.append(insert_player)
        self.player_list[-1].bb()
        print('{} is now big blind.'.format(self.player_list[1].name))
        self.player_list[-2].sb()
        print('{} is now small blind.'.format(self.player_list[2].name))
        self.player_list[-3].nb()

class Player:
    '''Player class'''
    def __init__(self, name, money=0):
        '''Initializes the Player class.
        @type self: Player
        @type name: str
        @type money: float
        '''
        assert type(name) == str
        assert type(money) == int or type(money) == float
        self.name = name
        self.money = money
        self.hand = []
        self.open_hand = True
        self.blind = None
    def __str__(self):
        if self.open_hand == True:
            if self.blind == 'b':
                return '{} ${} {} BB'.format(self.name, self.money, self.hand)
            elif self.blind == 's':
                return '{} ${} {} SB'.format(self.name, self.money, self.hand)
            else:
                return '{} ${} {}'.format(self.name, self.money, self.hand)
        else:
            if self.blind == 'b':
                return '{} ${} [??, ??] BB'.format(self.name, self.money, self.hand)
            elif self.blind == 's':
                return '{} ${} [??, ??] SB'.format(self.name, self.money, self.hand)
            else:
                return '{} ${} [??, ??]'.format(self.name, self.money)
    def __repr__(self):
        return 'Player({}, {})'.format(self.name, self.money)

    def bb(self):
        '''Become big blind.'''
        self.blind = 'b'
    def sb(self):
        '''Become small blind.'''
        self.blind = 's'
    def nb(self):
        '''Become no blind.'''
        self.blind = None
    def ante(self, required):
        '''Places ante (big or small blind) into pot. Subtracts from self.money'''
        self.money -= required
    def check(self, required):
        self.money -= required
        return required
    def raise_money(self, required, bet):
        assert bet >= required
        self.money -= bet
        return bet
    def fold(self):
        return 'fold'

    def reveal_hand(self):
        self.open_hand = True
    def hide_hand(self):
        self.open_hand = False

    #other methods below
    def add_card(self, card):
        '''Add a single Card to your hand self.hand.
        @type self: Player
        @type card: Card
        '''
        self.hand.append(card)
    def add_cards(self, card_list):
        '''Add each Card in card_list to your hand self.hand.
        @type self: Player
        @type card_list: list[Card]
        '''
        for card in card_list:
            self.hand.append(card)
    def pop_card(self, index):
        '''Remove a single Card at index index from hand self.hand and return it.
        @type self: Player
        @type index: int
        @rtype: Card
        '''
        self.hand.pop(index)
    def high_sort(self):
        '''Sort hand self.hand from highest to lowest'''
        temp_list = self.hand[:]
        temp_list.sort()
        self.hand = []
        for num in temp_list:
            self.hand.insert(0, num)
    def low_sort(self):
        '''Sort hand self.hand from lowest to highest'''
        self.hand.sort()
        

if __name__ == '__main__':
    p = Poker()
    a = Player('a', 100)
    b = Player('b', 100)
    c = Player('c', 100)
    d = Player('d', 100)
    p.add_players([a,b,c,d])
