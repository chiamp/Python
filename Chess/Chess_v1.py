class Board:
    def __init__(self):
        self.board = ['-' for i in range(64)]
        self.turn = 'w'
    def __str__(self):
        #return_list = ' abcdefgh\n'
        return_list = ''
        for i in range(len(self.board)):
            if i % 8 == 7 and i != 0:
                return_list += str(self.board[i]) + '\n'
            elif i % 8 == 0 or i == 0:
                return_list += str(8-(int(i / 8))) + str(self.board[i])
            else:
                return_list += str(self.board[i])
        return return_list + ' abcdefgh\n'
    def __repr__(self):
        return self.__str__()
    def fill_board(self):
        #self.board = ['rb','nb','bb','qb','kb','bb','nb','rb']
        #fill for black
        self.board[0], self.board[7] = Rook('black'), Rook('black')
        self.board[1], self.board[6] = Knight('black'), Knight('black')
        self.board[2], self.board[5] = Bishop('black'), Bishop('black')
        self.board[3] = Queen('black')
        self.board[4] = King('black')
        self.board[8], self.board[9], self.board[10], self.board[11], self.board[12], self.board[13], self.board[14], self.board[15] = Pawn('black'), Pawn('black'), Pawn('black'), Pawn('black'), Pawn('black'), Pawn('black'), Pawn('black'), Pawn('black')
        #fill for white
        self.board[56], self.board[63] = Rook('white'), Rook('white')
        self.board[57], self.board[62] = Knight('white'), Knight('white')
        self.board[58], self.board[61] = Bishop('white'), Bishop('white')
        self.board[59] = Queen('white')
        self.board[60] = King('white')
        self.board[48], self.board[49], self.board[50], self.board[51], self.board[52], self.board[53], self.board[54], self.board[55] = Pawn('white'), Pawn('white'), Pawn('white'), Pawn('white'), Pawn('white'), Pawn('white'), Pawn('white'), Pawn('white')


class Piece:
    def __init__(self, name, color):
        assert name in {'pawn', 'knight', 'bishop', 'rook', 'queen', 'king'}
        assert color in {'white', 'black'}
        self.name = name
        self.color = color

class Pawn(Piece):
    def __init__(self, color):
        Piece.__init__(self, 'pawn', color)
        self.value = 1
    def __repr__(self):
        return 'Pawn({})'.format(self.color)
    def __str__(self):
        if self.color == 'black':
            return 'p'
        else: #self.color == 'white'
            return 'P'
    def extensions(self):
        list_extensions = []
        
        pass
    def threaten(self):
        pass
class Rook(Piece):
    def __init__(self, color):
        Piece.__init__(self, 'rook', color)
        self.value = 1
    def __repr__(self):
        return 'Rook({})'.format(self.color)
    def __str__(self):
        if self.color == 'black':
            return 'r'
        else: #self.color == 'white'
            return 'R'
class Knight(Piece):
    def __init__(self, color):
        Piece.__init__(self, 'knight', color)
        self.value = 1
    def __repr__(self):
        return 'Knight({})'.format(self.color)
    def __str__(self):
        if self.color == 'black':
            return 'n'
        else: #self.color == 'white'
            return 'N'
class Bishop(Piece):
    def __init__(self, color):
        Piece.__init__(self, 'bishop', color)
        self.value = 1
    def __repr__(self):
        return 'Bishop({})'.format(self.color)
    def __str__(self):
        if self.color == 'black':
            return 'b'
        else: #self.color == 'white'
            return 'B'
class Queen(Piece):
    def __init__(self, color):
        Piece.__init__(self, 'queen', color)
        self.value = 1
    def __repr__(self):
        return 'Queen({})'.format(self.color)
    def __str__(self):
        if self.color == 'black':
            return 'q'
        else: #self.color == 'white'
            return 'Q'
class King(Piece):
    def __init__(self, color):
        Piece.__init__(self, 'king', color)
        self.value = 1
    def __repr__(self):
        return 'King({})'.format(self.color)
    def __str__(self):
        if self.color == 'black':
            return 'k'
        else: #self.color == 'white'
            return 'K'
