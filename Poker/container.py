class Container:
    '''General class Container'''
    def __init__(self):
        self.container = []
    def __repr__(self):
        return '{}'.format(self.container)
    def __str__(self):
        return '{}'.format(self.container)
    def __eq__(self, other):
        return self.container == other.container
    def __len__(self):
        return len(self.container)
    def append(self, obj):
        self.container.append(obj)
    def append_left(self, obj):
        self.container.insert(0, obj)
    def insert(self, index, obj):
        self.container.insert(index, obj)
    def append_group(self, group):
        for obj in group:
            self.container.append(obj)
    def append_left_group(self, group):
        for i in range(len(group)):
            self.container.insert(0+i, group[i])
    def insert_group(self, index, group):
        for i in range(len(group)):
            self.container.insert(index+i, group[i])
    def clear(self):
        for i in range(len(self.container)):
            self.container.pop()
    def pop(self, index=-1):
        '''Pop at index number'''
        return self.container.pop(index)
    def pop_left(self):
        return self.container.pop(0)
    def low_sort(self):
        '''Low to high'''
        self.container.sort()
    def high_sort(self):
        '''High to low'''
        temp_list = self.container[:]
        temp_list.sort()
        self.container = []
        for num in temp_list:
            self.container.insert(0, num)
    def reverse(self):
        '''Reverses current Container order'''
        temp_list = self.container[:]
        self.container = []
        for obj in temp_list:
            self.container.insert(0, obj)
    def shuffle(self):
#        from random import randint
#        temp_list = self.container[:]
#        self.container = []
#        while len(temp_list) != 0:
#            insert_obj = temp_list.pop(randint(0, len(temp_list)-1))
#            self.container.append(insert_obj)
        from random import shuffle
        shuffle(self.container)
