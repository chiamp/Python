from tkinter import *
from Sudoku import *


class FrameClass:
    def __init__(self, master):
        self.master = master
        self.board = None
        
        self.combinedFrame = Frame(master) #bottom of frame that also consists of two frames

        self.setupFrame = Frame(self.combinedFrame) #goes into combinedFrame
        self.buttonFrame = Frame(self.combinedFrame) #goes into combinedFrame

        self.textBox = Entry(self.setupFrame)
        self.textBox.pack(side=LEFT) #pack to setupFrame
        self.confirmButton = Button(self.setupFrame, text='OK', fg='green', command=self.initializeBoard)
        self.confirmButton.pack(side=RIGHT) #pack to setupFrame

        self.solveButton = Button(self.buttonFrame, text='SOLVE!', fg='red', command=self.solve)
        self.solveButton.pack(side=LEFT, fill=BOTH)

        self.puzzleFrame = PuzzleFrame(master, None, self.textBox) #top of frame
        #pack to root frame

        self.setupFrame.pack(side=TOP) #pack to combinedFrame
        self.buttonFrame.pack(side=BOTTOM) #pack to combinedFrame
        self.combinedFrame.pack(side=BOTTOM) #pack to root frame
        
    def initializeBoard(self):
        self.board = Board(int(self.textBox.get()))
        self.confirmButton.destroy()
        self.textBox.delete(0, END)

        self.puzzleFrame.setBoard(self.board)
        print(self.board)
        self.puzzleFrame.createTiles(self.board.edgeNumber)

    def solve(self):
        self.board.solve()
        for tilebutton in self.puzzleFrame.tileList:
            tilebutton.update()

class PuzzleFrame:
    def __init__(self, master, board, textBox):
        self.master = master
        self.board = None
        self.textBox = textBox
        self.puzzleFrame = Frame(master)
        self.puzzleFrame.pack(side=TOP)
        self.tileList = []
    def setBoard(self, board):
        self.board = board
    def createTiles(self, edgeLength):
        for row_num in range(edgeLength):
            for col_num in range(edgeLength):
                tilebutton = TileButton(self.board.getTile((row_num*edgeLength)+col_num), self.puzzleFrame, self.textBox)
                tilebutton.button.grid(row=row_num, column=col_num)
                self.tileList.append(tilebutton)

class TileButton:
    def __init__(self, tile, master, textBox):
        self.tile = tile
        self.value = tile.value
        self.master = master
        self.textBox = textBox
        self.button = Button(self.master, text=str(self), font=1, command=self.presetValue, width=5, height=2)
    def __str__(self):
        if self.value == '-':
            return ' '
        else:
            return self.value
    def presetValue(self):
        text = self.textBox.get()
        if text == '':
            self.tile.presetValue('-')
            self.button['text'] = ' '
        else:
            self.tile.presetValue(text)
            self.button['text'] = text
        self.textBox.delete(0, END)
    def update(self):
        if self.button['text'] != self.tile.value:
            self.button['text'] = self.tile.value

        
    

root = Tk()

frame = FrameClass(root)

root.mainloop()
