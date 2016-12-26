def reader(filename):
    '''Reads a string with filename as its file name, and returns a formatted dictionary x:y'''
    return_dict = {}
    with open(filename + '.txt', 'r') as file:
        line = file.readline()
        while line != '':
            return_dict[float(line.split()[0])] = float(line.split()[1])
            line = file.readline()
    return return_dict

import random
def random_eq_generator(limit=10, OC=0, r=10):
    '''limit the amount of characters for the equation
    OC specifies operator complexity. If True, it will include '//' and '%' operators
    r specifies range of numbers possible that can be randomly used
    Writes to a python file that will be read by the function run_eq(filename)
    Note this function is purely a random generator. Subsequent generators may use the evolve_generator function
    which will take into account how close the results are to alter the basic equation, or start from scratch'''
    char_limit = limit
    if OC == 0:
        operators = ['+','-','*','/','**']
    elif OC == 1:
        operators = ['+','-','*','/','**', '**(0.5)']
    else: #OC == 2
        operators = ['+','-','*','/','**','**(0.5)', '//','%']
    bracket_counter = 0 #if counter = 0, no ')' brackets can be generated
    #'(' increases counter by 1, while ')' decreases counter by 1
    #if the char_limit is <= 2, then no brackets can be generated
    #if char_limit = bracket_counter, then all remaining characters generated must be ')'

    #potentially useless lines below
    #brackets = ['(',')']
    #nums = [i for i in range(r)]

    curr_char = None #num/var must follow operator, open bracket
    #operator must follow num/var, closed bracket
    #closed bracket must follow num/var, closed bracket
    #open bracket must follow operator, open bracket

    return_str = ''
    t = random.randint(0,2)
    if t == 0:
        return_str += 'x ' #the variable we will be using
        curr_char = 'nv' #for number/variable
    elif t == 1:
        return_str += '( '
        bracket_counter += 1
        curr_char = 'ob' #for bracket
    else:
        return_str += str(random.randint(1,r)) + ' '
        curr_char = 'nv' #for number/variable

    char_limit -= 1

    while char_limit != 0:
        #deciding what curr_char will be 
        if curr_char == 'nv' or curr_char == 'cb':
            if (bracket_counter != 0 and char_limit == bracket_counter):
                curr_char = 'cb'
            elif char_limit == 1: 
                if bracket_counter >= 1:
                    curr_char = 'cb' #if we are at the last character it CANNOT be an operator
                else: #bracket_counter == 0
                    curr_char = 'NULL' #don't generate a character
            elif bracket_counter == 0: #meaning no open brackets ready to be closed
                curr_char = 'op'
            else:
                curr_char = ['op', 'cb'][random.randint(0,1)]
        else: #curr_char == 'op' or curr_char == 'ob'
            if char_limit <= 2 or bracket_counter >= char_limit // 2:
                curr_char = 'nv'
            else:
                curr_char = ['nv', 'ob'][random.randint(0,1)]

        #generating char based on curr_char
        if curr_char == 'op':
            return_str += operators[random.randint(0, len(operators)-1)] + ' '
        elif curr_char == 'cb':
            return_str += ') '
            bracket_counter -= 1
        elif curr_char == 'nv':
            t = random.randint(0,1)
            if t == 0:
                return_str += 'x '
            else:
                return_str += str(random.randint(1,r)) + ' '
        elif curr_char == 'ob':
            return_str += '( '
            bracket_counter += 1
        else: #curr_char = 'NULL'
            pass

        char_limit -= 1

    if bracket_counter >= 1:
        for i in range(bracket_counter):
            return_str += ') '
            
    return return_str
    
        

import os
def run_eq(filename):
    '''Reads and evaluates an equation in file filename and returns the result'''
    print('Evaluating {}.py'.format(filename))
    import filename
    filename.run() #filename can't be string; need to fix
