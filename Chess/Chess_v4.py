class Board:
    def __init__(self):
        self.board = ['-' for i in range(64)]
        self.turn = 'w'
    def __repr__(self):
        return_str = ''
        for row in range(8):
            for col in range(8):
                return_str += str(self.board[8*row + col])
            return_str += '\n'
        return return_str[:-1]
    def fill_board(self):
        for i in range(48,56):
            self.board[i] = Pawn('w', i)
    def empty_board(self):
        pass
    def restart_game(self):
        empty_board()
        fill_board()
        self.turn = 'w'
    def next_turn(self):
        if self.turn == 'w':
            self.turn = 'b'
        else:
            self.turn = 'w'
    def extensions(self):
        dict_extensions
        for piece in self.board:
            if piece != '-':
                pass

class Piece:
    def __init__(self, color, position):
        assert color in {'w', 'b'}
        assert type(position) == int
        self.color = color
        self.position = position
        self.row = (self.position // 8) + 1
        self.col = (self.position % 8) + 1
    def change_position(self, new_position):
        self.position = new_position
        self.row = (self.position // 8) + 1
        self.col = (self.position % 8) + 1
    def rowcol_convert(self, row, col):
        '''Converts a row and col input into a position integer'''
        return 8*(row-1) + col-1

class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.points = 1
    def __str__(self):
        return 'P'
    def __repr__(self):
        return "Pawn('{}', '{}', board)".format(self.color, self.position)
    def extensions(self):
        '''Returns a list of integers representing possible positions the Pawn can go to'''
        dict_extensions = {self.position:[]} #old_position:[possible new_positions]
        if self.color == 'w':
            dict_extensions[self.position].append(self.rowcol_convert(self.row-1, self.col)) #single jump
            if self.row == 2:
                dict_extensions[self.position].append(self.rowcol_convert(self.row-1, self.col)) #double jump
            dict_extensions[self.position].append(self.rowcol_convert(self.row-1, self.col-1)) #diagonal left capture
            dict_extensions[self.position].append(self.rowcol_convert(self.row+1, self.col+1)) #diagonal right capture
        return dict_extensions
    
                
b = Board()
b.fill_board()
