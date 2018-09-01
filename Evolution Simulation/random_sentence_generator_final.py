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
    #if points < 0: #if points are negative, just assume 0% fitness/similarity; there is no need for the degree/extent of how different it is from the goal string once its past a certain threshold
    #    points = 0
    return points
    #return points*100/(len(goal)*3) #multiply the length of string by 3 because each character in the string can score a maximum of 3 points

def evolution(goal, num_per_gen, top, mutation_rate, mutation_extent, power, translation_right, translation_up):
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

    #future loops for Generation 1+
    generation_counter = 0
    while highest_scores[0] != goal: #the 0 index in the highest_score list should have the highest score and thus be closest to the goal string
        #version 2.3 changed the way offspring per individual is distributed; before it used to be even among the top strings in highest_scores; now it can be defined by additional parameters for more diverse experiments/simulations
        offspring_tracker = mating_success(power, translation_right, translation_up, num_per_gen, highest_scores, goal)

        index = 0
        for string in highest_scores: #print the number offspring contibuted by the previous generation
            print("'{}' with {}% fitness/similarity contributed {} offspring for the next generation".format(string, (score(string, goal))*100/(len(goal)*3), offspring_tracker[index]))
            index += 1

        #now mutate each individual string a number of times equal to its corresponding integer value in offspring_tracker
        mutate_list = []
        
        #print(offspring_tracker)
        
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
    index = 0
    for string in highest_scores: #print the number offspring contibuted by the previous generation
            print("'{}' with {}% fitness/similarity will contribute {} offspring for the next generation".format(string, (score(string, goal))*100/(len(goal)*3), offspring_tracker[index]))
            index += 1
    print('Simulation complete')

def mating_success(power, translation_right, translation_up, num_per_gen, high_score_list, goal):
    '''Determine the offspring distribution proportional to how high their fitness/similarity is.
    For example, power = 0 would be uniform distribution, meaning each string/parent produces the same amount of offspring.
    power = 1 would be linear distribution, meaning each string/parent produces a number of offspring proportional to their relative fitness (their fitness compared to others in the population).
    power = 2 would be quadratic distribution, meaning reproductive success is highly skewed toward having higher
    Negative integers can also be used for the power argument if a higher-fitness-to-lower-reproductive-success relationship is wanted.
    Translations can be used to modify the distribution even further.
    If power > 0:
    The higher the translation_right > 0, the the higher reproductive success will be skewed towards higher fitness and will make offspring distribution less uniform.
    the lower the translation_right < 0 (meaning translation left), the lower reproductive success will be skewed toward higher fitness and will make the offspring distribution more uniform.
    The higher the translation_up > 0, the lower reproductive success will be skewed toward higher fitness and will make the offspring distribution more uniform.
    The lower the translation_up < 0 (meaning translation down), the higher reproductive success will be skewed towards higher fitness and will make offspring distribution less uniform.
    Precondition: If power = 0, then translation parameters don't matter, so it's good to keep them at 0
    @type power: float
    @type translation_right: float
    @type translation_up: float
    @type num_per_gen: int
    @type high_score_list: list[str]
    @type goal: str
    '''
    offspring_per_string_list = []
    for string in high_score_list:
        if score(string, goal) - translation_right < 0: #if it becomes negative, and power > 1, it becomes weird
            offspring_per_string_list.append(0)
        else:
            offspring_per_string_list.append(((score(string, goal) - translation_right)**power) + translation_up) #(((x-translation_right)**power) + translation_up), where x = score(string,goal)

    #print(offspring_per_string_list)
    
    total = 0
    for num in offspring_per_string_list:
        if num > 0: #if the number of offspring is greater than 0, add to total, otherwise no point in adding to the total if offspring produced is 0 or negative
            total += num

    balanced_list = [] #a list that contains the number of offspring each individual will produce, in proportion to the equation (((x-translation_right)**power) + translation_up)
    for num in offspring_per_string_list:
        if num > 0: #if the number is bigger than 0, divide by total offspring to get the ratio and multiply that to num_per_gen
            balanced_list.append(num_per_gen*(num/total)) #(num/total) is the ratio/proportion, num_per_gen is the number of offspring produced in total for next generation
        else: #if number is 0 or negative, no point
            balanced_list.append(0) #with this, it is possible that a translation downward can reduce all offspring produced by all generations to 0

    #print(balanced_list)
    
    total_remainder = 0
    if power == 0: #in the case of power = 0, which means the graph is a horizontal line, there's a chance that all strings will produce offspring with a fraction less than 0.5; thus when all the numbers are rounded a portion of offspring are lost
        for num in balanced_list:
            total_remainder += num % 1 #gather all the fractions of offspring
        total_remainder = round(total_remainder) #add them all together to see how much in total 'whole' offspring was lost due to rounding (it should add up to a whole number)

        for i in range(len(balanced_list)):
            balanced_list[i] = int(balanced_list[i]) #it is necessary to round down all the numbers even if they are greater than 0.5 because they will be added back on afterwards regardless
        
    balanced_list = helper_round(balanced_list) #round out all numbers so there are no decimals; you can't produce a fraction of an offspring

    if power == 0: #after the balanced_list has been rounded
        for i in range(total_remainder):
            balanced_list[i] += 1 #distribute the lost offspring from total_remainder giving priority to strings with higher fitness

    check_sum = 0
    index = 0
    while check_sum == 0 and index < len(balanced_list):
        check_sum += balanced_list[index]
        index += 1
    if check_sum == 0: #check_sum will be 0 by the end of the loop if everything in balanced_list is 0
       balanced_list[0] = num_per_gen #the first one on the balanced_list will produce 100% of the offspring because the first one on the balanced_list should have the highest fitness since it's based on the top list

    #print(balanced_list)

    return balanced_list

def helper_round(lst):
    '''
    Helper function for the function mating success. Rounds all values in the given list and returns a new list with the newly rounded values.
    Rounding consists of checking whether the decimal is above or under 0. If it is above 0, it will add that to the balance. If it is under 0, it will subtract it from the balance.
    If the remainder is 0.5, it will add 0.5 to the balance and subtract 0.5 from the balance every other time (starting with adding first).
    If, by the end of the function, the balance is greater than 0, that means that we have added more than we actually had, and need to subtract it from the end of the list.
    If, by the end of the function, the balance is less than 0, that means we have subtracted more than what we actually had, and need to add it to the beginning of the list.
    Adding and subtracting due to this, will result in adding 1 starting at either end of the list and moving inward until the balance reaches 0 again.
    This is to give priority to more fit individuals as the lst (from balanced_list) will have been sorted from highest fitness to lowest fitness.
    @type lst: list
    @rtype: list
    '''
    zero_balance = 0
    half_counter = 0
    new_list = []
    for num in lst:
        if num % 1 < 0.5:
            new_list.append(int(num))
            zero_balance += -(num % 1) #we took away its decimal, we have to pay it back somewhere else
        elif num % 1 > 0.5:
            new_list.append(round(num))
            zero_balance += 1 - (num % 1) #we added enough fraction/decimals to round up, we have to take an equal amount from elsewhere to balance it out
        else: #num % 1 == 0.5
            if half_counter % 2 == 0: #add 0.5 every other number that ends in .5, starting with the first time
                new_list.append(round(num + 0.5))
                zero_balance += 0.5 #must balance this surplus by taking away 0.5 from elsewhere
                half_counter += 1
            else: #take away 0.5 every other time
                new_list.append(round(num - 0.5))
                zero_balance += -0.5 #must balance this deficit by adding 0.5 elsewhere
                half_counter += -1
    
    zero_balance = round(zero_balance) #have to make it whole number
    
    if zero_balance > 0:
        for i in range(zero_balance):
            new_list[-zero_balance + i] += -1 #-zero_balance is the furthest from the end of new_list that needs a +1; then +i everytime to add +1 to the next number that needs it
    else: #zero_balance < 0
        for i in range(-zero_balance): #zero_balance is negative, so have to make it positive
            new_list[i] += 1
    return new_list

def run():
    goal = input('What is the string with 100% fitness? ')
    num_per_gen = int(input('How many individuals/strings per generation? '))
    top = int(input('How many individuals/strings survive to reproduce in the next generation? ' ))
    mutation_rate = float(input('What are the chances of a string mutating? '))
    mutation_extent = float(input('To what extent can a mutation mutate? '))
    power = input('Choose the power of the offspring distribution. ')
    translation_right = input('Choose how far the offspring distribution is translated to the right. ')
    translation_up = input('Choose how far the offspring distribution is translated upwards. ')
    if power == '':
        power = 0
    else:
        power = float(power)
    if translation_right == '':
        translation_right = 0
    else:
        translation_right = float(translation_right)
    if translation_up == '':
        translation_up = 0
    else:
        translation_up = float(translation_up)
    evolution(goal, num_per_gen, top, mutation_rate, mutation_extent, power, translation_right, translation_up)
    again = input('Run the simulation again? ')
    if again in {'yes', 'y', 'YES', 'Y', 'Yes'}:
        run()

run()

