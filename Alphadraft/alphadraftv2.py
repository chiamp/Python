class GeneralStats:
    '''General Statistics class for both the Player and Team class.
    @type team: str
    @type points: float
    @type salary: int    
    '''
    def __init__(self, team, points, salary):
        self.team = team
        self.points = points
        self.salary = salary
    def __eq__(self, other):
        return self.points == other.points
    def __lt__(self, other):
        return self.points < other.points
    def __gt__(self, other):
        return self.points > other.points

class Player(GeneralStats):
    '''Player class containing it's name, role, team name, points and salary.
    @type name: str
    @type role: str
    '''
    def __init__(self, name, role, team, points, salary):
        super().__init__(team, points, salary)
        self.name = name
        self.role = role
    def __str__(self):
        return '{}, {}, {}, {} points, ${}'.format(self.name, self.role, self.team, self.points, self.salary)

class Team(GeneralStats):
    '''Team class containing it's team name, salary, points, it's 5 players and the enemy team it's playing this week.
    @type top: Player
    @type jg: Player
    @type mid: Player
    @type adc: Player
    @type supp: Player
    @type enemy: Team    
    '''
    def __init__(self, team, points, salary, top, jg, mid, adc, supp): #excluded enemy parameter
        super().__init__(team, points, salary)
        self.top = top
        self.jg = jg
        self.mid = mid
        self.adc = adc
        self.supp = supp
        #self.enemy = enemy
        self.team_list = [self.top, self.jg, self.mid, self.adc, self.supp]
    def __str__(self):
        return '{}, {} points, ${}'.format(self.team, self.points, self.salary)
    def stats(self):
        print ('{}, {} points, ${}\n{}\n{}\n{}\n{}\n{}'.format(self.team, self.points, self.salary, self.top.__str__(), self.jg.__str__(), self.mid.__str__(), self.adc.__str__(), self.supp.__str__()))
def compile_data(filename):
    '''Take ctrl+a information from alphadraft.com and compile the data into a list of Team classes with Player classes inside the Team classes.
    @type filename: str as an address for a txt file
    @rtype: list[Teams]'''
    with open(filename, 'r') as file:
        line_counter = 0
        list_segments = []
        player_list = []
        team_list = []
        line = file.readline()
        while line.strip() != 'ALLTOPJNGMIDADCSUPFLEXTEAM Sort by Salary Show All Matchups':
            line = file.readline()
        line = file.readline()
        while line != 'TEAM\n':
            while line_counter % 10 != 9:
                if line_counter % 10 == 0:
                    role = line.strip()
                if line_counter % 10 == 2:
                    name = line.strip()
                if line_counter % 10 == 3:
                    list_segments = line.split()
                    team = list_segments[0]
                    #enemy = list_segments[2] #team class type or str?
                if line_counter % 10 == 6:
                    points = float(line)
                if line_counter % 10 == 8:
                    salary = int(line[1:2] + line[3:]) #take out dollar sign and comma
                line = file.readline()
                line_counter += 1
            player_list.append(Player(name, role, team, points, salary))
            line = file.readline()
            line_counter += 1

        #appending players onto teams from player_list
        line_counter = 0
        top, jg, mid, adc, supp = None, None, None, None, None
        while line != 'Your Team\n':
            while line_counter % 8 != 7:
                if line_counter % 8 == 1:
                    team = line.strip()
                if line_counter % 8 == 4:
                    points = float(line)
                if line_counter % 8 == 6:
                    salary = int(line[1:2] + line[3:])
                line = file.readline()
                line_counter += 1
            for player in player_list:
                if player.team == team:
                    if player.role == 'TOP':
                        top = player
                    if player.role == 'JNG':
                        jg = player
                    if player.role == 'MID':
                        mid = player
                    if player.role == 'ADC':
                        adc = player
                    if player.role == 'SUP':
                        supp = player
            team_list.append(Team(team, points, salary, top, jg, mid, adc, supp)) #excluded enemy argument'
            line = file.readline()
            line_counter += 1
        return team_list
        
class Draft:
    '''Draft class where you draft your roster.
    @type top: Player
    @type jg: Player
    @type mid: Player
    @type adc: Player
    @type supp: Player
    @type flex: Player
    @type team: Team
    precondition: cannot have more than three teams of the same (regardless if it is Player.team or Team.team)
    precondition: salary_remaining cannot be below 0
    '''
    def __init__(self, top, jg, mid, adc, supp, flex, team):
        self.salary_remaining = 50000 - (top.salary + jg.salary + mid.salary + adc.salary + supp.salary + flex.salary + team.salary)
        self.total_points = top.points + jg. points + mid.points + adc.points + supp.points + flex.points + team.points
        self.top = top
        self.jg = jg
        self.mid = mid
        self.adc = adc
        self.supp = supp
        self.flex = flex
        self.team = team
    def __str__(self):
        return '{}\n{}\n{}\n{}\n{}\n{}\n\n{}\n${} remaining salary\n{} total points\n'.format(self.top, self.jg, self.mid, self.adc, self.supp, self.flex, self.team, self.salary_remaining, self.total_points)
    def __eq__(self, other):
        return self.total_points == other.total_points
    def __lt__(self, other):
        return self.total_points < other.total_points
    def __gt__(self, other):
        return self.total_points > other.total_points
    def is_eligible(self):
       # if self.flex == (self.top or self.jg or self.mid or self.adc or self.supp):
       #     print("flex can't be used twice")
       # if self.salary_remaining < 0:
       #     print('salary is less than 0')
       # if three_or_less(self.top, self.jg, self.mid, self.adc, self.supp, self.flex, self.team) == False:
       #     print('more than three of the same team')
       # if self.flex != (self.top or self.jg or self.mid or self.adc or self.supp):
       #     print('eligible flex')
       # if self.salary_remaining >= 0:
       #     print('eligible salary')
       # if three_or_less(self.top, self.jg, self.mid, self.adc, self.supp, self.flex, self.team) == True:
       #     print('eligible team')
        return self.flex.name != self.top.name and self.flex.name != self.jg.name and self.flex.name != self.mid.name and self.flex.name != self.adc.name and self.flex.name != self.supp.name and self.salary_remaining >= 0 and three_or_less(self.top, self.jg, self.mid, self.adc, self.supp, self.flex, self.team)

def three_or_less(top, jg, mid, adc, supp, flex, team):
    '''Returns True if there are three or less of the same teams among all arguments.
    @type top: Player
    @type jg: Player
    @type mid: Player
    @type adc: Player
    @type supp: Player
    @type flex: Player
    @type team: Team
    @rtype: bool
    '''
    list_team = []
    list_team.append(top.team)
    list_team.append(jg.team)
    list_team.append(mid.team)
    list_team.append(adc.team)
    list_team.append(supp.team)
    list_team.append(flex.team)
    list_team.append(team.team)
    num_list = []


    '''length_team = len(list_team)
    v = 0

    current_team = list_team.pop(0)
    counter = 1
    while v < length_team:
        counter = 1
        x = v + 1
        while x < length_team:
            if list_team[i] == list_team[x]:
                counter += 1
                list_team.pop(x)
                length_team -= 1
            x += 1
    '''
    for team in list_team:
        counter = 0
        for i in range(len(list_team)):
            if team == list_team[i]:
                    counter += 1
        num_list.append(counter)
    for i in range(len(num_list)):
        if num_list[i] > 3:
            return False
    return True

def start_draft(filename, num_drafts, draft_teams):
    '''Start the draft based on eligible teams in draft_teams.
    Optional inputs for preferred teams. If none are filled, any team can be drafted. If any are filled, only the ones specified, will be drafted.
    Return a list of the top num_drafts highest scoring Draft classes.
    @type filename: str as an address for a txt file
    @type num_drafts: int
    @type draft_teams: list[str]
    @rtype: list[Draft]
    Precondition: num_drafts <= 10
    '''
    eligible_teams = []
    team_list = compile_data(filename)
    print('Data compiled')
    for team in team_list:
        if team.team in draft_teams:
            eligible_teams.append(team)
    if eligible_teams == []:
        eligible_teams = team_list
    print('Eligible teams determined')
    #eligible_teams now contains all eligible teams that can be drafted
    #now sort all eligible players in lists according to their positions
    top_list = []
    jg_list = []
    mid_list = []
    adc_list = []
    supp_list = []
    flex_list = []
    for team in eligible_teams:
        for player in team.team_list:
            flex_list.append(player)
            if player.role == 'TOP':
                top_list.append(player)
            if player.role == 'JNG':
                jg_list.append(player)
            if player.role == 'MID':
                mid_list.append(player)
            if player.role == 'ADC':
                adc_list.append(player)
            if player.role == 'SUP':
                supp_list.append(player)
    print('All players sorted')
    #now find all combinations of drafts | or put a limit as an option for an argument
    point_rankings_list = []
    counter = 0
    for top in top_list:
        for jg in jg_list:
            for mid in mid_list:
                for adc in adc_list:
                    for supp in supp_list:
                        for flex in flex_list:
                            for team in eligible_teams:
                                #print (Draft(top, jg, mid, adc, supp, flex, team))
                                #check to see Draft.is_eligible() is True and the Draft is not_in_list point_rankings_list
                                if Draft(top, jg, mid, adc, supp, flex, team).is_eligible(): #and not_in_list(Draft(top, jg, mid, adc, supp, flex, team), point_rankings_list):
                                    point_rankings_list.append(Draft(top, jg, mid, adc, supp, flex, team))
            counter += 1
            print('{}% combinations processed'.format(100*counter/((len(top_list)**2))))
    #now sort point_rankings_list in order of highest points to lowest points
    sorted_list = []    
    print('Now sorting...')
    for draft in point_rankings_list:
        i = 0
        if sorted_list != []:
            if not_in_list(draft, sorted_list) == True:
                while draft < sorted_list[i] and i < 9: #will stop sorting after the top 10
                    i += 1
                    if i == len(sorted_list): #if i <= 9 and i is equal to the length of the sorted list (can only be true if list has not reached maximum length of 10 yet)
                        sorted_list.append(draft) #append the draft
                if draft > sorted_list[i] and i < 9: #if draft points greater than current draft in sorted_list
                    sorted_list.insert(i, draft) #insert it before the current draft in sorted_list
                    if len(sorted_list) == 11: #if list size is greater than 10 after insertion
                        sorted_list.pop() #pop the last term as it is the draft with the smallest points
                #if draft <= sorted_list and i == 9, do nothing as the draft points are too small to be included in the list and we have reached the end of the list
        elif sorted_list == []:
            sorted_list.append(draft)

    print('Function complete\n')
    #return the top num_drafts in sorted_list
    return sorted_list[:num_drafts]

def not_in_list(draft_compare, lst):
    '''Returns True if the draft_compare is not in the list of drafts. This checks regardless of roles, so for example, a certain combination of flex and supp or vice versa, is the same.
    @type draft: Draft
    @type lst: list[Draft]
    @rtype: bool
    '''
    for draft in lst:
        if draft.team.team == draft_compare.team.team:
            if (draft.top.name or draft.flex.name) == draft_compare.top.name:
                if (draft.jg.name or draft.flex.name) == draft_compare.jg.name:
                    if (draft.mid.name or draft.flex.name) == draft_compare.mid.name:
                        if (draft.adc.name or draft.flex.name) == draft_compare.adc.name:
                            if (draft.supp.name or draft.flex.name) == draft_compare.supp.name:
                                #[top, jg, mid, adc, supp][flex]
                                #at this point we know that [a b c d e][f] vs. [a/f b/f c/f d/f e/f][?]
                                if (draft_compare.top.name or draft_compare.flex.name) == draft.top.name:                                    
                                    if (draft_compare.jg.name or draft_compare.flex.name) == draft.jg.name:
                                        if (draft_compare.mid.name or draft_compare.flex.name) == draft.mid.name:
                                            if (draft_compare.adc.name or draft_compare.flex.name) == draft.adc.name:
                                                if (draft_compare.supp.name or draft_compare.flex.name) == draft.supp.name:                                                    
                                                    #at this point we know that [a b c d e][f] vs. [a b c d e][?] or [f b c d e][a]
                                                    #[a b c d e][f] vs. [f b c d e ][a] is already False
                                                    #the only possibility that can still be True is if f != ? given that [a b c d e] == [a b c d e]
                                                    #in any other scenario, it is False
                                                    if draft.top.name == draft_compare.top.name:
                                                        if draft.jg.name == draft_compare.jg.name:
                                                            if draft.mid.name == draft_compare.mid.name:
                                                                if draft.adc.name == draft_compare.adc.name:
                                                                    if draft.supp.name == draft_compare.supp.name:                                                                        
                                                                        #at this point we know that [a b c d e] == [a b c d e]
                                                                        #and that it can't be [a b c d e][f] vs. [f b c d e][a]
                                                                        if draft.flex.name == draft_compare.flex.name: #if [f] == [?]
                                                                            return False #then we know that [a b c d e][f] == [a b c d e][?=f]
                                                                        #if [f] != [?]
                                                                        else:
                                                                           pass #the flex of the two drafts are different and therefore it is not False
                                                                    else:
                                                                        return False
                                                                else:
                                                                    return False
                                                            else:
                                                                return False
                                                        else:
                                                            return False
                                                    else:
                                                        return False
                                                    
                                    
                                    
                                '''
                                #at this point we know that [a b c d e][f] vs. [a/f b/f c/f d/f e/f][?]
                                #Case 1: if all positions are the same and flex is different
                                #[a b c d e][f] vs. [a b c d e][T]
                                if draft.top.name == draft_compare.top.name and draft.jg.name == draft_compare.jg.name and draft.mid.name == draft_compare.mid.name and draft.adc.name == draft_compare.adc.name and draft.supp.name == draft_compare.supp.name:
                                    if draft.flex.name == draft_compare.flex.name:
                                        return False
                                #Case 2: if draft1's flex is used in a position in draft2, and draft 2's flex is used in a position in draft1
                                #[a b c d e][f] vs. [f b c d e][a]
                                if draft.flex.name == draft_compare.top.name or draft.flex.name == draft_compare.jg.name or draft.flex.name == draft_compare.mid.name or draft.flex.name == draft_compare.adc.name or draft.flex.name == draft_compare.supp.name:
                                    if draft_compare.flex.name == draft.top.name or draft_compare.flex.name == draft.jg.name or draft_compare.flex.name == draft.mid.name or draft_compare.flex.name == draft.adc.name or draft_compare.flex.name == draft.supp.name: 
                                        return False'''
                                
    return True


def run():
    print('Welcome to Alphadraft Simulator, by Marcus Chiam!')
    filename = input('What is the filename? ') + '.txt'
    available_teams = compile_data(filename)
    print('Here are the available teams:')
    for team in available_teams:
        print(team.team)
    team_pool = input('What are the teams that you want to draft? If you want to draft all teams, press Enter. Otherwise, enter the teams you want to draft with a space inbetween each one. ')
    team_list = team_pool.split()
    num_drafts = int(input('How many drafts would you like to see (maximum 10)? '))
    draft_list = start_draft(filename, num_drafts, team_list)
    #print("Displaying draft rates for the top draft. The following players' statistics are based on the top {} drafts:\n{} {}%\n{} {}%\n{} {}%\n{} {}%\n{} {}%\n{} {}%\n".format(num_drafts, draft_list[0].top, 
    for draft in draft_list:
        print(draft)

run()
