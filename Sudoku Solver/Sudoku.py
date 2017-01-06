import math

class Tile:
    def __init__(self, value, position=-1):
        self.value = value #can be '-' or a number string (e.g. '3')
        self.position = position
        self.pn = [] #possible numbers
        self.npn = [] #not possible numbers
        self.row = None
        self.column = None
        self.box = None
    def __str__(self):
        return self.value
    def __repr__(self):
        return self.value
    def setPosition(self, position):
        self.position = position
    def getPosition(self):
        return self.position
    def isComplete(self):
        return self.value != '-'
    def getPN(self):
        return self.pn
    def addPN(self, num):
        self.pn.append(num)
    def addPNs(self, lst):
        for num in lst:
            self.addPN(num)
    def removePN(self, num):
        self.pn.remove(num)
    def clearPN(self):
        self.pn = []
    def getNPN(self):
        return self.npn
    def addNPN(self, num):
        self.npn.append(num)
    def addNPNs(self, lst):
        for num in lst:
            self.addNPN(num)
    def removeNPN(self, num):
        self.npn.remove(num)
    def clearNPN(self, lst):
        self.npn = []
    def assignNPN(self): #check each row/column/box that this tile is part of and assign NPN
        for num in (self.row.getHave() + self.column.getHave() + self.box.getHave()):
            if num not in self.getNPN():
                self.addNPN(num)
                if num in self.getPN():
                    self.removePN(num)
    def assignPN(self): #check each row/column/box that this tile is part of and assign PN
        for num in (self.row.getMissing() + self.column.getMissing() + self.box.getMissing()):
            if (num not in self.getNPN()) and (num not in self.getPN()):
                self.addPN(num)
    def getValue(self):
        return self.value
    def setValue(self, value):
        self.value = value #self.isComplete() should equal True now so this tile should not show up when calling the .getIncompleteTiles() method
        #after setting it to a value, update all the PNs and NPNs that are in the same row/column/box
        #i.e. remove the value from PN and add the value to NPN for all affected tiles
        checkList = []
        for tile in (self.row.getIncompleteTiles() + self.column.getIncompleteTiles() + self.box.getIncompleteTiles()):
            if tile not in checkList:
                checkList.append(tile)
                if value in tile.getPN():
                    tile.removePN(value)
                if value not in tile.getNPN():
                    tile.addNPN(value)
    def presetValue(self, value):
        self.value = value
    def check(self):
        if len(self.getPN()) == 1:
            self.setValue(self.getPN()[0])
        elif self.checkOnlyPossible(self.row.getAllPN()):
            pass
        elif self.checkOnlyPossible(self.column.getAllPN()):
            pass
        elif self.checkOnlyPossible(self.box.getAllPN()):
            pass
        elif self.checkLineElim():
            pass
        elif self.row.checkNakedPair():
            pass
        elif self.column.checkNakedPair():
            pass
        elif self.box.checkNakedPair():
            pass
    def checkOnlyPossible(self, checkList):
        for num in self.getPN():
            if checkList.count(num) == 1: #if a certain value is only possible at this tile, it will only show up once in the list
                self.setValue(num) #therefore it must be that value
                return True
        return False
    def checkLineElim(self):
        #if there are 3 or less of the same number in box.getAllPN()
        for num in self.box.getMissing():
            if self.box.getAllPN().count(num) <= 3:
                #check if the Tiles who carry that number in their PN is in the same row or column
                #if they are, remove that number from the PN of all other tiles in that same ContainmentTile that are not from that box and add that number to their NPN
                samePNTiles = self.box.findTiles(num)
                if self.row.allBelong(samePNTiles):
                    for tile in self.row.getIncompleteTiles():
                        if tile not in samePNTiles and num in tile.getPN():
                            tile.removePN(num)
                            tile.addNPN(num)
                    return True
                elif self.row.allBelong(samePNTiles):
                    for tile in self.column.getIncompleteTiles():
                        if tile not in samePNTiles and num in tile.getPN():
                            tile.removePN(num)
                            tile.addNPN(num)
                    return True
        return False
        

class Board:
    def __init__(self, edgeNumber=9): #edgeNumber must be a perfect square
        self.edgeNumber = edgeNumber
        self.square = int(math.sqrt(self.edgeNumber))
        self.board = []
        #below are lists that contain the TileContainers
        self.row = []
        self.column = []
        self.box = []
        for i in range(self.edgeNumber**2):
            self.board.append(Tile('-', i))
        for i in range(self.edgeNumber):
            self.createRow(i+1)
            self.createColumn(i+1)
            self.createBox(i+1)

    def __str__(self):
        return_str = ''
        for i in range(len(self.board)):
            return_str += self.board[i].value
            if (i+1)%self.square == 0:
                return_str += ' '
            if (i+1)%self.edgeNumber == 0:
                return_str += '\n'
            if (i+1)%(self.edgeNumber*self.square) == 0:
                return_str += '\n'
        return return_str[:-1]
    def createRow(self, num): #num represents row number to a max of self.edgeNumber and min of 1
        self.row.append(Row([tile for tile in self.board[((num-1)*self.edgeNumber):((num-1)*self.edgeNumber)+self.edgeNumber]]))
    def createColumn(self, num): #num represents column number to a max of self.edgeNumber and min of 1
        self.column.append(Column([self.board[i] for i in range(len(self.board)) if ((i+1-num)%self.edgeNumber==0)]))
    def createBox(self, num): #num represents box number to a max of self.edgeNumber and min of 1
        topLeftNum = ((num-1)//self.square)*(self.edgeNumber*self.square) + (self.square)*((num-1)%self.square)
        listIndex = []
        for i in range(self.square): #row num
            for x in range(self.square): #column num
                listIndex.append(topLeftNum+(i*self.edgeNumber)+x)
        self.box.append(Box([self.board[i] for i in listIndex]))
    def presetTile(self, position, value): #setting tile values without assigning/altering PN and NPN numbers yet
        self.getTile(position).value = value
    def getTile(self, position):
        return self.board[position]
    def setTileValue(self, position, value):
        self.getTile(position).setValue(value)
    def getIncompleteTiles(self):
        return [tile for tile in self.board if not tile.isComplete()]
    def getCompleteTiles(self):
        return [tile for tile in self.board if tile.isComplete()]
    def assignNPN(self): #for every incomplete tile
        for tile in self.getIncompleteTiles():
            tile.assignNPN()
    def assignPN(self): #for every incomplete tile
        for tile in self.getIncompleteTiles():
            tile.assignPN()
    def check(self):
        for tile in self.getIncompleteTiles():
            tile.check()
    def isSolved(self):
        return len(self.getIncompleteTiles()) == 0
    def solve(self):
        print('Calculating possible values...')
        self.assignNPN()
        self.assignPN()

        print('Solving...')
        while not self.isSolved():
            self.check()
            print(self)

class TileContainer:
    def __init__(self, listTiles=[]):
        self.listTiles = listTiles
        self.addMulParent(listTiles)
    def __repr__(self):
        return str(self.listTiles)
    def addTile(self, tile):
        self.listTiles.append(tile)
        self.addParent(tile)
    def addTiles(self, listTiles):
        for tile in listTiles:
            self.addTile(tile)
    def addParent(self, tile):
        #to be overrided by child classes
        pass
    def addMulParent(self, listTiles):
        for tile in listTiles:
            self.addParent(tile)
    def getTiles(self):
        return self.listTiles
    def getIncompleteTiles(self):
        return [tile for tile in self.listTiles if tile.value == '-']
    def getCompleteTiles(self):
        return [tile for tile in self.listTiles if tile.value != '-']
    def getMissing(self):
        checkList = []
        for i in range(len(self.listTiles)):
            checkList.append(str(i+1))
        for tile in self.getCompleteTiles():
            checkList.remove(tile.value)
        return checkList
    def getHave(self):
        return [tile.value for tile in self.getCompleteTiles()]
    def getAllPN(self):
        checkList = []
        for tile in self.getIncompleteTiles():
            checkList += tile.getPN() #add all possible numbers of all incomplete tiles in a TileContainer to a list
        return checkList
    def findTiles(self, PN): #find all incomplete Tiles in this TileContainer with a specific PN
        return_list = []
        for tile in self.getIncompleteTiles():
            if PN in tile.getPN():
                return_list.append(tile)
        return return_list
    def allBelong(self, tileList): #check to see if all tiles in tileList belong to the same TileContainer
        for tile in tileList:
            if tile not in self.getTiles():
                return False
        return True
    def checkNakedPair(self):
        twoPNList = []
        #check to see if there are a pair of Tiles whose .getPN() is length 2
        for tile in self.getTiles():
            if len(tile.getPN()) == 2:
                twoPNList.append(tile)
        #if there are, compare them to see if their PN's are the same
        if len(twoPNList) >= 2: #can't compare anything if there's only one tile
            for i in range(len(twoPNList)-1): #the last one doesn't have anything to compare to
                firstNum = twoPNList[i].getPN()[0]
                secondNum = twoPNList[i].getPN()[1]
                for x in range(i+1, len(twoPNList)): #tile twoPNList[i] will compare with everything in front of it (or rather, everything further back into the list)
                    if firstNum in twoPNList[x].getPN() and secondNum in twoPNList[x].getPN():
                        #if they are, remove those PN's from all other tiles in the same TileContainer
                        removeChecker = False #check to see if something was removed
                        for tile in self.getIncompleteTiles():
                            if tile != twoPNList[i] and tile != twoPNList[x]:
                                if firstNum in tile.getPN():
                                    tile.removePN(firstNum)
                                    tile.addNPN(firstNum)
                                    removeChecker = True
                                if secondNum in tile.getPN():
                                    tile.removePN(secondNum)
                                    tile.addNPN(secondNum)
                                    removeChecker = True
                        return removeChecker
        return False

class Row(TileContainer):
    def __init__(self, listTiles=[]):
        super().__init__(listTiles)
    def addParent(self, tile):
        tile.row = self
class Column(TileContainer):
    def __init__(self, listTiles=[]):
        super().__init__(listTiles)
    def addParent(self, tile):
        tile.column = self
class Box(TileContainer):
    def __init__(self, listTiles=[]):
        super().__init__(listTiles)
    def addParent(self, tile):
        tile.box = self

def coordinate(column, row, edgeNumber): #returns corresponding position index number
    return column-1 + (row-1)*edgeNumber

if __name__ == '__main__':
    b = Board(int(input('Input board size. Must be a perfect square. ')))
    print(b)
    commandList = input('Input tiles to fill. Format (column)(row)(value). ').split()
    for command in commandList: #command in format (column)(row)(value)
        b.presetTile((coordinate(int(command[0]), int(command[1]), b.edgeNumber)), command[2:])
    print(b)
    input('Press Enter to start solving. ')

    b.solve()
