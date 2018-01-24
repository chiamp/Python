from datetime import *

class Money:
    def __init__(self,value):
        if value >= 0:
            self.pos = True
        else:
            self.pos = False
        self.dollars = self.get_dollars(value)
        self.cents = self.get_cents(value)
        self.value = self.dollars + self.cents
    def get_dollars(self,value):
        if self.pos == True:
            return int(value//1)
        else:
            return -int(value//-1)
    def get_cents(self,value):
        if self.pos == True:
            return round(value%1,2)
        else:
            return round(value%-1,2)
    def str_cents(self):
        x = str(self.cents)
        if len(x) == 1:
            return '00'
        if self.pos == True:
            if len(x) == 3:
                return str(x)[-1] + '0'
            else:
                return str(x[-2:])
        else:
            if len(x) == 4:
                return str(x)[-1] + '0'
            else:
                return str(x[-2:])
    def __str__(self):
        if self.pos == True:
            return '${}.{}'.format(self.dollars,self.str_cents())
        else:
            return '-${}.{}'.format(-self.dollars,self.str_cents())
    def __repr__(self):
        return str(self)
    def __add__(self,other):
        return Money(self.value+other.value)
    def __sub__(self,other):
        return Money(self.value-other.value)
    def __mul__(self,other):
        return Money(self.value*other)
    def __truediv__(self,other):
        return Money(self.value/other)
    def __gt__(self,other):
        return self.value > other.value
    def __lt__(self,other):
        return self.value < other.value

class Entry:
    def __init__(self,cost=Money(0),title='',category='',description='',date=date.today()):
        self.date = date
        self.cost = cost #cost argument must be of type Money
        self.category = category
        self.title = title
        self.description = description
    def __str__(self):
        return '{}\t{}\t{}\t{}\t{}'.format(str(self.date),str(self.cost),self.category,self.title,self.description)
    def __repr__(self):
        return str(self)

class Logbook:
    def __init__(self,log=[]):
        self.log = log
        self.filename = 'logbook.txt'
    def __str__(self):
        return_str = '\n'
        for entry in self.log:
            return_str += str(entry) + '\n'
        return return_str[:-1]
    def __repr__(self):
        return str(self)
    def add_entry(self,entry):
        self.log.append(entry)
    def push_entry(self,entry):
        with open(self.filename,'a') as file:
            file.write(str(entry) + '\n')
    def push_entries(self,entry_list):
        with open(self.filename,'a') as file:
            for entry in entry_list:
                file.write(str(entry) + '\n')
    def push_log(self):
        self.push_entries(self.log)
        self.log.clear()
    def backup_log(self):
        with open(self.filename,'r') as read_file:
            with open('backup_{}.txt'.format(date.today()),'w') as write_file:
                write_file.write(read_file.read())
        print('Backed up log to backup_{}.txt'.format(date.today()))
    def pull_log(self):
        self.log.clear()
        with open(self.filename,'r') as file:
            line = file.readline()
            while line != '':
                data = line.split('\t')
                self.add_entry(Entry(date=date(int(data[0][:4]),int(data[0][5:7]),int(data[0][8:])),cost=Money(float(data[1][1:])),category=data[2],title=data[3],description=data[4][:-1]))
                line = file.readline()
    def pull_categories(self,category_list):
        self.log.clear()
        with open(self.filename,'r') as file:
            line = file.readline()
            while line != '':
                data = line.split('\t')
                if data[2] in category_list:
                    self.add_entry(Entry(date=date(int(data[0][:4]),int(data[0][5:7]),int(data[0][8:])),cost=Money(float(data[1][1:])),category=data[2],title=data[3],description=data[4][:-1]))
                line = file.readline()
    def pull_dates(self,from_date,end_date=date.today()):
        self.log.clear()
        with open(self.filename,'r') as file:
            line = file.readline()
            while line != '':
                data = line.split('\t')
                if from_date <= (date(int(data[0][:4]),int(data[0][5:7]),int(data[0][8:]))) <= end_date:
                    self.add_entry(Entry(date=date(int(data[0][:4]),int(data[0][5:7]),int(data[0][8:])),cost=Money(float(data[1][1:])),category=data[2],title=data[3],description=data[4][:-1]))
                line = file.readline()
    def pull_expenses_over(self,value):
        self.log.clear()
        with open(self.filename,'r') as file:
            line = file.readline()
            while line != '':
                data = line.split('\t')
                if float(data[1][1:]) > value:
                    self.add_entry(Entry(date=date(int(data[0][:4]),int(data[0][5:7]),int(data[0][8:])),cost=Money(float(data[1][1:])),category=data[2],title=data[3],description=data[4][:-1]))
                line = file.readline()
    def pull_expenses_under(self,value):
        self.log.clear()
        with open(self.filename,'r') as file:
            line = file.readline()
            while line != '':
                data = line.split('\t')
                if float(data[1][1:]) < value:
                    self.add_entry(Entry(date=date(int(data[0][:4]),int(data[0][5:7]),int(data[0][8:])),cost=Money(float(data[1][1:])),category=data[2],title=data[3],description=data[4][:-1]))
                line = file.readline()
    def get_categories(self,category_list):
        new_log = []
        for entry in self.log:
            if entry.category in category_list:
                new_log.append(entry)
        return new_log
    def get_neg_categories(self,category_list):
        new_log = []
        for entry in self.log:
            if entry.category not in category_list:
                new_log.append(entry)
        return new_log
    def get_locations(self,location_list):
        new_log = []
        for entry in self.log:
            if entry.title in location_list:
                new_log.append(entry)
        return new_log
    def get_neg_locations(self,location_list):
        new_log = []
        for entry in self.log:
            if entry.title not in location_list:
                new_log.append(entry)
        return new_log
    def get_dates(self,from_date,end_date=date.today()):
        new_log = []
        for entry in self.log:
            if from_date <= entry.date <= end_date:
                new_log.append(entry)
        return new_log
    def get_expenses_over(self,value):
        v = Money(value)
        new_log = []
        for entry in self.log:
            if entry.cost > v:
                new_log.append(entry)
        return new_log
    def get_expenses_under(self,value):
        v = Money(value)
        new_log = []
        for entry in self.log:
            if entry.cost < v:
                new_log.append(entry)
        return new_log
    def get_expenses_interval(self,interval=30):
        return_str = '\n'
        d = timedelta(interval-1)
        from_date = date.today() - d
        end_date = date.today()
        return_str += '==== {} to {} ====\n'.format(date_string(from_date),date_string(end_date))
        total = Money(0)
        i = len(self.log)-1
        while i >= 0:
            if from_date <= self.log[i].date <= end_date:
                return_str += str(self.log[i]) + '\n'
                total += self.log[i].cost
                i -= 1
            else:
                return_str += 'TOTAL COST: {}\n\n'.format(total)
                total = Money(0)
                end_date = from_date - timedelta(1)
                from_date -= d + timedelta(1)
                return_str += '==== {} to {} ====\n'.format(date_string(from_date),date_string(end_date))
        return_str += 'TOTAL COST: {}'.format(total)
        print(return_str)
    def get_expenses_month(self):
        return_str = '\n'
        from_date = date.today() - timedelta(date.today().day-1)
        end_date = date.today()
        return_str += '==== {} to {} ====\n'.format(date_string(from_date),date_string(end_date))
        total = Money(0)
        i = len(self.log)-1
        while i >= 0:
            if from_date <= self.log[i].date <= end_date:
                return_str += str(self.log[i]) + '\n'
                total += self.log[i].cost
                i -= 1
            else:
                return_str += 'TOTAL COST: {}\n\n'.format(total)
                total = Money(0)
                end_date = from_date - timedelta(1)
                from_date -= timedelta(1)
                from_date -= timedelta(from_date.day-1)
                return_str += '==== {} to {} ====\n'.format(date_string(from_date),date_string(end_date))
        return_str += 'TOTAL COST: {}'.format(total)
        print(return_str)
    def get_expenses_day(self,day):
        new_log = []
        for entry in self.log:
            if entry.date.isoweekday() == day:
                new_log.append(entry)
        return new_log
    def get_total(self):
        total = Money(0)
        for entry in self.log:
            total += entry.cost
        return total
    def sort_decreasing_date(self):
        pass
    def sort_increasing_date(self):
        pass
    def prompt_menu(self):
        print('\n==== Main Menu ====')
        print('1. View entire logbook')
        print('2. Filter by categories')
        print('3. Filter by dates')
        print('4. Filter by cost')
        print('5. Filter by locations')
        print('6. Filter by day of the week')
        print('7. View expenses by month')
        print('8. View expenses by custom interval')
        print('9. Add an entry')
        i = input('')
        if i == '1':
            print(self)
            self.prompt_menu()
        elif i == '2':
            self.prompt_categories()
        elif i == '3':
            self.prompt_dates()
        elif i == '4':
            self.prompt_cost()
        elif i == '5':
            self.prompt_locations()
        elif i == '6':
            self.prompt_expenses_day()
        elif i == '7':
            self.get_expenses_month()
            self.prompt_menu()
        elif i == '8':
            self.prompt_expenses_interval()
            self.prompt_menu()
        elif i == '9' or i == '':
            self.prompt_entry()
        else:
            self.prompt_menu()
    def prompt_options(self):
        print('\n==== Options ====')
        print('1. Return to main menu')
        print('2. Filter by categories')
        print('3. Filter by dates')
        print('4. Filter by cost')
        print('5. Filter by locations')
        print('6. Filter by day of the week')
        print('7. View expenses by month')
        print('8. View expenses by custom interval')
        i = input('')
        if i == '1':
            self.pull_log()
            self.prompt_menu()
        elif i == '2':
            self.prompt_categories()
        elif i == '3':
            self.prompt_dates()
        elif i == '4':
            self.prompt_cost()
        elif i == '5':
            self.prompt_locations()
        elif i == '6':
            self.prompt_expenses_day()
        elif i == '7':
            self.get_expenses_month()
            self.prompt_menu()
        elif i == '8':
            self.prompt_expenses_interval()
            self.prompt_options()
        else:
            self.prompt_options()
    def prompt_categories(self):
        category_list = input('List categories: ').split()
        if category_list[0] == '-':
            self.log = self.get_neg_categories(category_list[1:])
        else:
            self.log = self.get_categories(category_list)
        print(self)
        self.prompt_options()
    def prompt_dates(self):
        print('Format either YYYY-MM-DD or type a number indicating how many days ago to today')
        start_date = input('Start date: ')
        if start_date == '':
            start_date = date.today()
        elif '-' not in start_date:
            start_date = date.today() - timedelta(int(start_date))
        else:
            data = start_date.split(sep='-')
            start_date = date(int(data[0]),int(data[1]),int(data[2]))
        end_date = input('End date: ')
        if end_date == '':
            end_date = date.today()
        elif '-' not in end_date:
            end_date = date.today() - timedelta(int(end_date))
        else:
            data = end_date.split(sep='-')
            end_date = date(int(data[0]),int(data[1]),int(data[2]))
        self.log = self.get_dates(start_date,end_date)
        print(self)
        self.prompt_options()
    def prompt_cost(self):
        answer = input('Type either > or < followed by a number to filter by cost: ')
        if answer[0] == '>':
            self.log = self.get_expenses_over(float(answer[1:]))
        else:
            self.log = self.get_expenses_under(float(answer[1:]))
        print(self)
        self.prompt_options()
    def prompt_locations(self):
        location_list = input('List locations: ').split()
        if location_list[0] == '-':
            self.log = self.get_neg_locations(location_list[1:])
        else:
            self.log = self.get_locations(location_list)
        print(self)
        self.prompt_options()
    def prompt_expenses_interval(self):
        self.get_expenses_interval(int(input('Set the number of days in each interval: ')))
    def prompt_expenses_day(self):
        self.log = self.get_expenses_day(int(input('Which day of the week: ')))
        print(self)
        self.prompt_options()
    def prompt_entry(self):
        answer = input('Days ago: ')
        if answer == '':
            d = date.today()
        else:
            d = date.today() - timedelta(int(answer))
        cost = Money(float(input('Cost: ')))
        category = input('Category: ')
        title = input('Location: ')
        description = input('Description: ')
        entry = Entry(cost,title,category,description,d)
        self.push_entry(entry)
        print('Entry pushed to {}'.format(self.filename))
        self.add_entry(entry)
        self.prompt_menu()

month_list = ['January','February','March','April','May','June','July','August','September','October','November','December']

def date_string(dt):
    month = month_list[dt.month-1]
    return '{} {}, {}'.format(month,dt.day,dt.year)
def month_string(dt):
    month = month_list[dt.month-1]
    return '{} {}'.format(month,dt.year)

if __name__ == '__main__':
    l = Logbook()
    #l.backup_log()
    l.pull_log()
    l.prompt_menu()
