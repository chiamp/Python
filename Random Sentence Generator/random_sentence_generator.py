def create_dict(char_list):
    pass

def generate(required_char=None, exact_char=None, length=None):
    '''Generate a random string of random length. Optional arguments include a dictionary for required_char (but no exact position), a dictionary for exact_char (positions known) and fixed length.
    The required_char dictionary consists of a character representing a key, pointing to the number of times it must exist in the generated string.
    Required characters just need the character to exist in the string, so if for example, the same character is required in the exact_char dictionary, there will be no need to add the same char again.
    The exact_char dictionary consists of an integer representing an index as a key, pointing to the corresponding string character which is to be placed in the generated string.
    @type required_char: dict[str:int]
    @type exact_char: dict[int:str]
    @type length: int
    @rtype: str
    '''
    return_str = ''
    from random import randint
    if required_char == None:
        if exact_char == None:
            if length == None: #if no parameters were given
                i = randint(31,126) #chr(31) is just used as an indicator to stop writing; it is never going to be written. The real writing range is from 32 to 126 inclusive.
                while i != 31:
                    return_str += chr(i)
                    i = randint(31,126)
            else: #length must have a value at this point
                current_length = 0
                while current_length != length:
                    i = randint(32,126) #no need for chr(31) as a stop indicator
                    return_str += chr(i)
                    current_length += 1
        else: #exact_char is not None
            if length == None:
                minimum_length = len(exact_char) #minimum_length equal to the length of exact_char dictionary
                i = randint(31,126) #chr(31) is just used as an indicator to stop writing; it is never going to be written. The real writing range is from 32 to 126 inclusive.
                while i != 31 or len(return_str) < minimum_length:
                    if i != 31:
                        return_str += chr(i)
                    i = randint(31,126)
                #below, is the code for when exact_char is not None
                return_str_copy = '' #building a new string with exact_char and positions and to be copied onto return_str
                index = 0
                for char in return_str:
                    if index in exact_char: #looking to see if the index is ak ey in the dictionary exact_char
                        return_str_copy += exact_char[index]
                        index += 1
                    else: #index is not in the exact_char, so add the char normally
                        return_str_copy += char
                        index += 1
                return_str = return_str_copy #copy the new str into return_str
            else: #length is not None and exact_char is not None
                current_length = 0
                while current_length != length:
                    i = randint(32,126) #no need for chr(31) as a stop indicator
                    return_str += chr(i)
                    current_length += 1
                #below, is the code for when exact_char is not None
                return_str_copy = '' #building a new string with exact_char and positions and to be copied onto return_str
                index = 0
                for char in return_str:
                    if index in exact_char: #looking to see if the index is ak ey in the dictionary exact_char
                        return_str_copy += exact_char[index]
                        index += 1
                    else: #index is not in the exact_char, so add the char normally
                        return_str_copy += char
                        index += 1
                return_str = return_str_copy #copy the new str into return_str
    
    else: #required_char is not None
        locked_indexes = set() #to keep track of which indexes cannot be overwritten by characters from required_char(_copy)
        if exact_char == None:
            if length == None:
                minimum_length = 0
                for key in required_char:
                    minimum_length += required_char[key] #to find the minimum length of the string
                i = randint(31,126) #chr(31) is just used as an indicator to stop writing; it is never going to be written. The real writing range is from 32 to 126 inclusive.
                while i != 31 or len(return_str) < minimum_length:
                    if i != 31:
                        return_str += chr(i)
                    i = randint(31,126)
                #below, is the code for when required_char is not None
                required_char_copy = required_char.copy() #make a copy of required_char dict because dictionaries are mutable and you don't want to modify the original
                index = 0
                for char in return_str:
                    if char in required_char_copy: #if the char is in the required_char_copy dict
                        required_char_copy[char] += -1 #subtract one as one less is needed to fulfill the required character condition
                        locked_indexes.add(index) #this char cannot be overwritten so lock its index in locked_indexes
                        if required_char_copy[char] == 0: #if the char now requires 0
                            required_char_copy.pop(char) #remove the key as the condition has been fulfilled
                    index += 1
                #by now the remaining characters in required_char_copy have not been fulfilled and must be inserted
                new_dict = {} #new dictionary for remaining required characters that are randomly assigned indexes in the format of index:char
                for req_char in required_char_copy:
                    while required_char_copy[req_char] != 0: #have to keep assigning a random index to this req_char until the number of times it is required to appear is fulfilled
                        i = randint(0, len(return_str)-1) #find a random index to insert the req_char
                        while i in locked_indexes and len(locked_indexes) < len(return_str): #if i is the same as a locked index
                            i = randint(0, len(return_str)-1) #find another random index
                        locked_indexes.add(i) #this randomly chosen index cannot be overwritten by others now; otherwise if randint picks this same index again, you will lose one copy of the req_char
                        new_dict[i] = req_char #add a new entry to new_dict with index as the key, pointing to the req_char
                        required_char_copy[req_char] += -1 #after assigning an index to it once, subtract by 1 the number of times needed to repeat this process
                #at this point the new_dict contains all information for which to insert the required characters into the randomly assigned index
                temp_list = [] #since str does not support index assignments, we must use a list to first store each individual character of return_str, and then use index assignments to assign the req_char in new_dict
                for char in return_str:
                    temp_list.append(char)  
                #temp_list has all char of return_str now as individual objects in the list
                for index in new_dict:
                    temp_list[index] = new_dict[index] #assigning a new char to the randomly selected indexes
                temp_str = '' #temporary string to be copied to return_str
                for char in temp_list:
                    temp_str += char
                return_str = temp_str
            else: #length is not None
                current_length = 0
                while current_length != length:
                    i = randint(32,126) #no need for chr(31) as a stop indicator
                    return_str += chr(i)
                    current_length += 1
                #below, is the code for when required_char is not None
                required_char_copy = required_char.copy() #make a copy of required_char dict because dictionaries are mutable and you don't want to modify the original
                index = 0
                for char in return_str:
                    if char in required_char_copy: #if the char is in the required_char_copy dict
                        required_char_copy[char] += -1 #subtract one as one less is needed to fulfill the required character condition
                        locked_indexes.add(index) #this char cannot be overwritten so lock its index in locked_indexes
                        if required_char_copy[char] == 0: #if the char now requires 0
                            required_char_copy.pop(char) #remove the key as the condition has been fulfilled
                    index += 1
                #by now the remaining characters in required_char_copy have not been fulfilled and must be inserted
                new_dict = {} #new dictionary for remaining required characters that are randomly assigned indexes in the format of index:char
                for req_char in required_char_copy:
                    while required_char_copy[req_char] != 0: #have to keep assigning a random index to this req_char until the number of times it is required to appear is fulfilled
                        i = randint(0, len(return_str)-1) #find a random index to insert the req_char
                        while i in locked_indexes and len(locked_indexes) < len(return_str): #if i is the same as a locked index
                            i = randint(0, len(return_str)-1) #find another random index
                        locked_indexes.add(i) #this randomly chosen index cannot be overwritten by others now; otherwise if randint picks this same index again, you will lose one copy of the req_char
                        new_dict[i] = req_char #add a new entry to new_dict with index as the key, pointing to the req_char
                        required_char_copy[req_char] += -1 #after assigning an index to it once, subtract by 1 the number of times needed to repeat this process
                #at this point the new_dict contains all information for which to insert the required characters into the randomly assigned index
                temp_list = [] #since str does not support index assignments, we must use a list to first store each individual character of return_str, and then use index assignments to assign the req_char in new_dict
                for char in return_str:
                    temp_list.append(char)  
                #temp_list has all char of return_str now as individual objects in the list
                for index in new_dict:
                    temp_list[index] = new_dict[index] #assigning a new char to the randomly selected indexes
                temp_str = '' #temporary string to be copied to return_str
                for char in temp_list:
                    temp_str += char
                return_str = temp_str
        else: #exact_char is not None (and required_char not None)
            required_char_copy = required_char.copy() #make a copy of required_char dict because dictionaries are mutable and you don't want to modify the original
            for index in exact_char:
                if exact_char[index] in required_char_copy: #if both dictionaries share the same character
                    required_char_copy[exact_char[index]] += -1 #reduce required_char_copy's requirement for the existence of that character by one
                    if required_char_copy[exact_char[index]] == 0: #if the character's requirement is 0
                        required_char_copy.pop(exact_char[index]) #remove the character key from the dictionary
            #by this point, required_char_copy dictioanry has been reduced and there should be no overlaps of characters (before characters are randomly generated, where there may be more instances of overlap)
            if length == None:
                minimum_length = len(exact_char) #minimum_length equal to the length of exact_char dictionary
                #all characters in exact_char are accounted for
                for key in required_char:
                    minimum_length += required_char[key] #required_char[key] gives you the number of times it is supposed to exist in the string
                i = randint(31,126) #chr(31) is just used as an indicator to stop writing; it is never going to be written. The real writing range is from 32 to 126 inclusive.
                while i != 31 or len(return_str) < minimum_length:
                    if i != 31:
                        return_str += chr(i)
                    i = randint(31,126)
                #below, is the code for when exact_char is not None
                return_str_copy = '' #building a new string with exact_char and positions and to be copied onto return_str
                index = 0
                for char in return_str:
                    if index in exact_char: #looking to see if the index is ak ey in the dictionary exact_char
                        return_str_copy += exact_char[index]
                        locked_indexes.add(index) #this index cannot be overwritten
                        index += 1
                    else: #index is not in the exact_char, so add the char normally
                        return_str_copy += char
                        index += 1
                return_str = return_str_copy #copy the new str into return_str
                #below, is the code for when required_char is not None
                required_char_copy = required_char.copy() #make a copy of required_char dict because dictionaries are mutable and you don't want to modify the original
                index = 0
                for char in return_str:
                    if char in required_char_copy: #if the char is in the required_char_copy dict
                        required_char_copy[char] += -1 #subtract one as one less is needed to fulfill the required character condition
                        locked_indexes.add(index) #this char cannot be overwritten so lock its index in locked_indexes
                        if required_char_copy[char] == 0: #if the char now requires 0
                            required_char_copy.pop(char) #remove the key as the condition has been fulfilled
                    index += 1
                #by now the remaining characters in required_char_copy have not been fulfilled and must be inserted
                new_dict = {} #new dictionary for remaining required characters that are randomly assigned indexes in the format of index:char
                for req_char in required_char_copy:
                    while required_char_copy[req_char] != 0: #have to keep assigning a random index to this req_char until the number of times it is required to appear is fulfilled
                        i = randint(0, len(return_str)-1) #find a random index to insert the req_char
                        while i in locked_indexes and len(locked_indexes) < len(return_str): #if i is the same as a locked index
                            i = randint(0, len(return_str)-1) #find another random index
                        locked_indexes.add(i) #this randomly chosen index cannot be overwritten by others now; otherwise if randint picks this same index again, you will lose one copy of the req_char
                        new_dict[i] = req_char #add a new entry to new_dict with index as the key, pointing to the req_char
                        required_char_copy[req_char] += -1 #after assigning an index to it once, subtract by 1 the number of times needed to repeat this process
                #at this point the new_dict contains all information for which to insert the required characters into the randomly assigned index
                temp_list = [] #since str does not support index assignments, we must use a list to first store each individual character of return_str, and then use index assignments to assign the req_char in new_dict
                for char in return_str:
                    temp_list.append(char)  
                #temp_list has all char of return_str now as individual objects in the list
                for index in new_dict:
                    temp_list[index] = new_dict[index] #assigning a new char to the randomly selected indexes
                temp_str = '' #temporary string to be copied to return_str
                for char in temp_list:
                    temp_str += char
                return_str = temp_str
            else: #length is not None (and exact_char and required_char not None)
                current_length = 0
                while current_length != length:
                    i = randint(32,126) #no need for chr(31) as a stop indicator
                    return_str += chr(i)
                    current_length += 1
                #below, is the code for when exact_char is not None
                return_str_copy = '' #building a new string with exact_char and positions and to be copied onto return_str
                index = 0
                for char in return_str:
                    if index in exact_char: #looking to see if the index is ak ey in the dictionary exact_char
                        return_str_copy += exact_char[index]
                        locked_indexes.add(index) #this index cannot be overwritten
                        index += 1
                    else: #index is not in the exact_char, so add the char normally
                        return_str_copy += char
                        index += 1
                return_str = return_str_copy #copy the new str into return_str
                #below, is the code for when required_char is not None
                required_char_copy = required_char.copy() #make a copy of required_char dict because dictionaries are mutable and you don't want to modify the original
                index = 0
                for char in return_str:
                    if char in required_char_copy: #if the char is in the required_char_copy dict
                        required_char_copy[char] += -1 #subtract one as one less is needed to fulfill the required character condition
                        locked_indexes.add(index) #this char cannot be overwritten so lock its index in locked_indexes
                        if required_char_copy[char] == 0: #if the char now requires 0
                            required_char_copy.pop(char) #remove the key as the condition has been fulfilled
                    index += 1
                #by now the remaining characters in required_char_copy have not been fulfilled and must be inserted
                new_dict = {} #new dictionary for remaining required characters that are randomly assigned indexes in the format of index:char
                print(locked_indexes)
                for req_char in required_char_copy:
                    while required_char_copy[req_char] != 0: #have to keep assigning a random index to this req_char until the number of times it is required to appear is fulfilled
                        i = randint(0, len(return_str)-1) #find a random index to insert the req_char
                        while i in locked_indexes and len(locked_indexes) < len(return_str): #if i is the same as a locked index and if length of locked_indexes is less than length of return_str (to prevent an infinite loop below)
                            #print('line 4')
                            i = randint(0, len(return_str)-1) #find another random index
                            #print('line 5')
                        locked_indexes.add(i) #this randomly chosen index cannot be overwritten by others now; otherwise if randint picks this same index again, you will lose one copy of the req_char
                        new_dict[i] = req_char #add a new entry to new_dict with index as the key, pointing to the req_char
                        required_char_copy[req_char] += -1 #after assigning an index to it once, subtract by 1 the number of times needed to repeat this process
                #at this point the new_dict contains all information for which to insert the required characters into the randomly assigned index
                temp_list = [] #since str does not support index assignments, we must use a list to first store each individual character of return_str, and then use index assignments to assign the req_char in new_dict
                for char in return_str:
                    temp_list.append(char)  
                #temp_list has all char of return_str now as individual objects in the list
                for index in new_dict:
                    temp_list[index] = new_dict[index] #assigning a new char to the randomly selected indexes
                temp_str = '' #temporary string to be copied to return_str
                for char in temp_list:
                    temp_str += char
                return_str = temp_str
    return return_str

def score(string, goal):
    '''Returns a score of the string based on how similar it is to the goal in terms of length, presence of same characters, and whether those characters are in the right position.
    @type string: str
    @type goal: str
    @rtype: float
    '''
    points = 0
    points += -abs(len(string) - len(goal)) #-1 points for every difference between length of strings
    
    temp_dict = {}
    for char in goal: #make a dictionary for goal
        if char in temp_dict:
            temp_dict[char] += 1
        else:
            temp_dict[char] = 1
    for char in string:
        if char in temp_dict:
            points += 2 #+2 points if the character in string is present in goal (represented by temp_dict)
            temp_dict[char] += -1
            if temp_dict[char] == 0:
                temp_dict.pop(char) #once the count reaches 0, we want to remove the key so that it won't proc the char in temp_dict if statement
            
    for i in range(len(goal)): #no point in exceeding index of goal to compare positions
        if i <= len(string)-1: #can't index past the range of string
            if goal[i] == string[i]:
                points += 2 #+2 additional points if the character is in the same position (adding up to +4 points in total)
    #print(points)
    return points/(len(goal)*4)


def mutation(string, rate):
    '''Mutate the string at a certain rate.
    Rate determines the chance at which a change occurs, as well as the extent of the change if it does occur.
    Akin to asexual reproduction with random mutations.
    @type string: str
    @type rate: float
    @rtype: str
    '''
    from random import randint

    #below is code for mutating already written characters in the string
    string_list = []
    for char in string:
        string_list.append(char) #append string characters to string_list so that we can use index assignments for mutations
    for i in range(len(string_list)):
        if randint(0,100) <= rate: #if random chance is meets the mutation rate requirement
            id_num = ord(string_list[i])
            range_difference = round(47*rate/100) #47 is half of the range between 32 and 126
            low_end = id_num - range_difference
            high_end = id_num + range_difference
            chr_num = randint(low_end, high_end) #replace that character with a random integer
            if chr_num < 32:
                chr_num = 126 - (31 - chr_num) #loop to the end if it's under 32
            if chr_num > 126:
                chr_num = 32 + (127 - chr_num) #loop to the beginning if it's over 126
            string_list[i] = chr(chr_num)
    new_string = ''
    for char in string_list:
        new_string += char

    #below is code for mutating the length of the string
    while randint(0,100) <= rate: #while the mutation rate is being met, alter the length of the string
        if randint(0,100) <= 50: #if less than 50%
            new_string = new_string[:-1] #take away one character at the end of the string
        else: #if more than 50%
            new_string += chr(randint(32,126)) #add a random character to the end of the string

    return new_string

def mutation_original(string, rate):
    #original plan was to have it return a list of dict,dict,int to input in generate function
    #but maybe use mutation to generate new functions?
    pass

def recombination(list_string, rate):
    '''This would be crossing previous generations' parameter/variables; i.e. sexual reproduction'''
    for string in list_string:
        lst = mutation(string, rate)
    
def run(goal, num_per_gen, rate, top=None):
    mutate_list = []
    highest_score = ''
    for i in range(num_per_gen):
        mutate_list.append(generate())
    for string in mutate_list:
        if score(string, goal) > score(highest_score, goal):
            highest_score = string
    while highest_score != goal:
        mutate_list = []
        for i in range(num_per_gen):
            mutate_list.append(mutation(highest_score, rate))
        for string in mutate_list:
            if score(string, goal) > score(highest_score, goal):
                highest_score = string
        #print(mutate_list)
        print("'{}' was the highest scoring string, with a {}% similarity to the goal string '{}'".format(highest_score, score(highest_score, goal)*100, goal))
