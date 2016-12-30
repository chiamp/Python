import rps_ai
from imp import reload

class Game:
    '''Rock, paper, scissors game'''
    def __init__(self):
        self.self = self
    def play(self, user, ai):
        '''Evaluates both user and ai input and determines winner
        @type user: str
        @type ai: str
        @rtype: str
        '''
        if user == 'r':
            if ai == 'r':
                return "It's a draw!"
            if ai == 'p':
                return 'The AI wins!'
            if ai == 's':
                return 'You win!'
        if user == 'p':
            if ai == 'p':
                return "It's a draw!"
            if ai == 's':
                return 'The AI wins!'
            if ai == 'r':
                return 'You win!'
        if user == 's':
            if ai == 's':
                return "It's a draw!"
            if ai == 'r':
                return 'The AI wins!'
            if ai == 'p':
                return 'You win!'
        
def run():
    reload(rps_ai)
    g = Game()
    a = rps_ai.ai()
    usermove = input('Input user move. ')
    aimove = a.response(usermove)
    print(aimove)
    who_wins = g.play(usermove, aimove)
    a.result(who_wins, aimove, usermove)
    return who_wins
