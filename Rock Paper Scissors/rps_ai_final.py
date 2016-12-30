r_draw = True
p_draw = True
s_draw = True

class ai:
    def __init__(self):
        self.draw = []
        #self.response = ['r', 'p', 's']
    def result(self, wl, aimove, user_move):
        '''Alters its own coding if it loses. wl is an indicator of win/loss.
        user_move is the user's last move.
        @type wl: str
        @type user_move: str
        '''
        if wl == 'You win!': #aka the user wins and the AI lost
            with open('rps_ai.py', 'r') as file:
                code_list = file.readlines()
            insertion = "        if user_move == '{}'".format(user_move) + ":\n            possible_responses.remove('{}')".format(aimove) + "\n"
            #insertion is based on the following code to be inserted after a loss
            #if user_move == 'r':
            #   possible_responses.remove('{}'.format(self.last_move))
            #   self.last_move = possible_responses[randint(0, len(possible_responses)-1)]
            code_list.insert(-2, insertion)
            with open('rps_ai.py', 'w') as file:
                for line in code_list:
                    file.write(line)
        if wl == "It's a draw!":
            if aimove == 'r' and r_draw == None:
                with open('rps_ai.py', 'r') as file:
                    code_list = file.readlines()
                insertion = "        if user_move == '{}'".format(user_move) + ":\n            possible_responses.remove('{}')".format(aimove) + "\n"
                code_list.insert(-2, insertion)
                code_list[0] = 'r_draw = True\n'
                with open('rps_ai.py', 'w') as file:
                    for line in code_list:
                        file.write(line)
        if wl == "It's a draw!":
            if aimove == 'p' and p_draw == None:
                with open('rps_ai.py', 'r') as file:
                    code_list = file.readlines()
                insertion = "        if user_move == '{}'".format(user_move) + ":\n            possible_responses.remove('{}')".format(aimove) + "\n"
                code_list.insert(-2, insertion)
                code_list[1] = 'p_draw = True\n'
                with open('rps_ai.py', 'w') as file:
                    for line in code_list:
                        file.write(line)
        if wl == "It's a draw!":
            if aimove == 's' and s_draw == None:
                with open('rps_ai.py', 'r') as file:
                    code_list = file.readlines()
                insertion = "        if user_move == '{}'".format(user_move) + ":\n            possible_responses.remove('{}')".format(aimove) + "\n"
                code_list.insert(-2, insertion)
                code_list[2] = 's_draw = True\n'
                with open('rps_ai.py', 'w') as file:
                    for line in code_list:
                        file.write(line)
    def response(self, user_move):
        '''Responds to the user's move with its own move
        @type user: str
        @rtype: str
        '''
        from random import randint
        possible_responses = ['r', 'p', 's']
        if user_move == 'r':
            possible_responses.remove('s')
        if user_move == 'r':
            possible_responses.remove('r')
        if user_move == 's':
            possible_responses.remove('p')
        if user_move == 's':
            possible_responses.remove('s')
        if user_move == 'p':
            possible_responses.remove('p')
        if user_move == 'p':
            possible_responses.remove('r')
        self.last_move = possible_responses[randint(0, len(possible_responses)-1)]
        return self.last_move
