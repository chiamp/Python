def generate():
    '''Generate a random string of random length.
    @rtype: str
    '''
    return_str = ''
    from random import randint
    i = randint(31,126) #chr(31) is just used as an indicator to stop writing; it is never going to be written. The real writing range is from 32 to 126 inclusive.
    while i != 31:
        return_str += chr(i)
        i = randint(31,126)
    return return_str

def mutation(string, mutation_rate, mutation_extent):
    '''Mutate the string at a chance of mutation_rate. If it does get mutated, mutate it at an extent of mutation_extent.
    Akin to asexual reproduction with random mutations.
    Precondition: mutation_rate < 100 (otherwise, an infinite loop will occur when determining mutations in length)
    @type string: str
    @type mutation_rate: float
    @type mutation_extent
    @rtype: str
    '''
    from random import randint
    #below is code for mutating already written characters in the string
    string_list = []
    for char in string:
        string_list.append(char) #append string characters to string_list so that we can use index assignments for mutations
    for i in range(len(string_list)):
        if randint(0,100) <= mutation_rate: #if random chance is meets the mutation rate requirement
            id_num = ord(string_list[i])
            range_difference = round(47*mutation_extent/100) #47 is half of the range between 32 and 126
            low_end = id_num - range_difference
            high_end = id_num + range_difference
            chr_num = randint(low_end, high_end) #replace that character with a random integer
            if chr_num < 32:
                chr_num = 126 - (31 - chr_num) #loop to the end if it's under 32
            if chr_num > 126:
                chr_num = 32 + (chr_num - 127) #loop to the beginning if it's over 126
            string_list[i] = chr(chr_num)
    new_string = ''
    for char in string_list:
        new_string += char

    #below is code for mutating the length of the string
    while randint(0,100) <= (mutation_rate + mutation_extent)/2: #while the average between mutation_rate and mutation_extent is being met, alter the length of the string
        if randint(0,100) <= 50: #if less than 50%
            new_string = new_string[:-1] #take away one character at the end of the string
        else: #if more than 50%
            new_string += chr(randint(32,126)) #add a random character to the end of the string

    return new_string

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
    for i in range(len(goal)): #no point in exceeding index of goal to compare positions
        if i <= len(string)-1: #can't index past the range of string
            if goal[i] == string[i]:
                points += 3 #+3 points if the character is in the same position
    #print(points)
    return points*100/(len(goal)*3) #multiply the length of string by 3 because each character in the string can score a maximum of 3 points

def evolution(goal, num_per_gen, top, mutation_rate, mutation_extent):
    '''Simulate evolution. Define a goal str that represents 100% similarity (or maximum fitness).
    Define the number of strings produced per generation, num_per_gen.
    Define the number of top strings in a generation that will survive and contribute to the next generation.
    Define the mutation_rate and mutation_extent.
    Return a list of strings in the current generation and a string that states the top strings that will survive and contribute to the next generation.
    @type goal: str
    @type num_per_gen: int
    @type top: int
    @type mutation_rate: float
    @type mutation_extent: float
    @rtype: list[str] | str
    '''
    #preliminary set up for Generation 0
    mutate_list = []
    highest_scores = []
    for i in range(num_per_gen): #fills out mutate_list
        mutate_list.append(generate())
    for string in mutate_list:
        if len(highest_scores) == 0: #if highest_scores is empty
            highest_scores.append(string)
        elif 0 < len(highest_scores) < top: #if the length of highest_scores list is not equal to the length of top
            index = 0
            while index < len(highest_scores) and score(string, goal) <= score(highest_scores[index], goal): #cycle through indexes until you either find a highest_score thats lower than current string, or you run out of index and reach the end of the highest_scores list
                index += 1
            if index < len(highest_scores) and score(string, goal) > score(highest_scores[index], goal): #if index is still smaller than length of highest_scores list and the current string score is higher than the current highest_scores string score
                highest_scores.insert(index, string) #insert the current string before the current highest_scores strings
            else: #otherwise, if the index is greater than the length of the highest_scores list (meaning the string score is not larger than any of the strings currently in highest_scores list), just append it to the end of the list
                highest_scores.append(string)
        else: #for when the highest_scores list is full and is equal to the length of top
            index = 0
            while index < top and score(string, goal) <= score(highest_scores[index], goal):
                index += 1
            if index < top and score(string, goal) > score(highest_scores[index], goal): #have to make sure the index is not equal or greater than top, otherwise we will get an error when we try finding highest_scores[index]
                highest_scores.insert(index, string)
                highest_scores.pop()
    print('\nGeneration 0')
    print(mutate_list)
    for string in highest_scores:
        print("'{}' with {}% similarity/fitness".format(string, score(string, goal)))

    #future loops for Generation 1+
    generation_counter = 0
    while highest_scores[0] != goal: #the 0 index in the highest_score list should have the highest score and thus be closest to the goal string
        offspring_per_individual = num_per_gen // top
        remainder = num_per_gen % top
        offspring_tracker = []
        for i in range(top):
            offspring_tracker.append(offspring_per_individual)
        for i in range(remainder):
            offspring_tracker[i] += 1 #remainder gets distributed so that an individual produces one additional offspring starting from highest fitness and going downward
        #now mutate each individual string a number of times equal to offspring_per_individual
        mutate_list = []
        for i in range(top): #highest_scores list and offspring_tracker list should be same length since they are both based on the argument top
            for offspring_num in range(offspring_tracker[i]): #the integer of offspring_tracker[i] dictates how many times the corresponding string highest_scores[i] will mutate
                mutate_list.append(mutation(highest_scores[i], mutation_rate, mutation_extent))

        highest_scores = [] #reset every generation; meaning even if the parents from the previous generation are more fit than their offspring, they will not be in highest_scores list; only the offspring can be in the list
        for string in mutate_list:
            if len(highest_scores) == 0: #if highest_scores is empty
                highest_scores.append(string)
            elif 0 < len(highest_scores) < top: #if the length of highest_scores list is not equal to the length of top
                index = 0
                while index < len(highest_scores) and score(string, goal) <= score(highest_scores[index], goal): #cycle through indexes until you either find a highest_score thats lower than current string, or you run out of index and reach the end of the highest_scores list
                    index += 1
                if index < len(highest_scores) and score(string, goal) > score(highest_scores[index], goal): #if index is still smaller than length of highest_scores list and the current string score is higher than the current highest_scores string score
                    highest_scores.insert(index, string) #insert the current string before the current highest_scores strings
                else: #otherwise, if the index is greater than the length of the highest_scores list (meaning the string score is not larger than any of the strings currently in highest_scores list), just append it to the end of the list
                    highest_scores.append(string)
            else: #for when the highest_scores list is full and is equal to the length of top
                index = 0
                while index < top and score(string, goal) <= score(highest_scores[index], goal):
                    index += 1
                if index < top and score(string, goal) > score(highest_scores[index], goal): #have to make sure the index is not equal or greater than top, otherwise we will get an error when we try finding highest_scores[index]
                    highest_scores.insert(index, string)
                    highest_scores.pop()
        generation_counter += 1
        print('\nGeneration {}'.format(generation_counter))
        print(mutate_list)
        for string in highest_scores:
            print("'{}' with {}% fitness/similarity".format(string, score(string, goal)))

#evolution('marcus', 50, 2, 40, 40)

def run():
    goal = input('What is the string with 100% fitness? ')
    num_per_gen = int(input('How many individuals/strings per generation? '))
    top = int(input('How many individuals/strings survive to reproduce in the next generation? ' ))
    mutation_rate = float(input('What are the chances of a string mutating? '))
    mutation_extent = float(input('To what extent can a mutation mutate? '))
    evolution(goal, num_per_gen, top, mutation_rate, mutation_extent)
