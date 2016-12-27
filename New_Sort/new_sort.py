def new_sort(lst):
    '''Precondition: all values in list lst are int or float'''
    counter_list = []
    negative_list = []
    for num in lst:
        if num >= 0: #positive number or 0
            if num >= len(counter_list): #number bigger than length of list
                loop = num - len(counter_list) + 1
                while loop >= 2: #extend length of list
                    counter_list.append(0)
                    loop += -1
                counter_list.append(1)
            else:
                counter_list[num] += 1
        else: #negative number
            if num*(-1) > len(negative_list): #[-5, -4, -3, -2, -1]
                loop = num*(-1) - len(negative_list)
                while loop >= 2:
                    negative_list.insert(0, 0)
                    loop += -1
                negative_list.insert(0, 1)
            else:
                negative_list[len(negative_list) + num] += 1
    return_list = []
    for i in range(len(negative_list)):
        counter = 0
        while counter < negative_list[i]:
            return_list.append(-len(negative_list) + i)
            counter += 1
    for i in range(len(counter_list)):
        counter = 0
        while counter < counter_list[i]:
            return_list.append(i)
            counter += 1
    return return_list

a = list(range(10000000))
from random import shuffle
shuffle(a)
b = a[:]
c = a[:]
d = a[:]
l = [5,4,3,2,1]
import cProfile
