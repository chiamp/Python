class Board:
    def __init__(self):
        self.board = ['-' for i in range(64)]
        #self.white_points, self.black_points = 0, 0
        self.turn = None
        #self.white_check, self.black_check = None, None
        self.castle_dict = {0: True, 4: True, 7: True, 56: True, 60: True, 63: True} #False if a piece moved
    def __str__(self):
        #return_list = ' abcdefgh\n'
        return_list = ''
        for i in range(len(self.board)):
            if i % 8 == 7 and i != 0:
                return_list += str(self.board[i]) + '\n'
            elif i % 8 == 0 or i == 0:
                return_list += str(8-(int(i / 8))) + ' ' + str(self.board[i])
            else:
                return_list += str(self.board[i])
        return return_list + '  abcdefgh'
    def __repr__(self):
        return self.__str__()
    def fill_board(self):
        #self.board = ['rb','nb','bb','qb','kb','bb','nb','rb']
        #fill for black
        self.board[0], self.board[7] = 'r', 'r'
        self.board[1], self.board[6] = 'n', 'n'
        self.board[2], self.board[5] = 'b', 'b'
        self.board[3] = 'q'
        self.board[4] = 'k'
        self.board[8], self.board[9], self.board[10], self.board[11], self.board[12], self.board[13], self.board[14], self.board[15] = 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'
        #fill for white
        self.board[56], self.board[63] = 'R', 'R'
        self.board[57], self.board[62] = 'N', 'N'
        self.board[58], self.board[61] = 'B', 'B'
        self.board[59] = 'Q'
        self.board[60] = 'K'
        self.board[48], self.board[49], self.board[50], self.board[51], self.board[52], self.board[53], self.board[54], self.board[55] = 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'
    def start_game(self):
        self.turn = 'white'
        #self.white_check, self.black_check = False, False
        print('Game begins.')
    def next_turn(self):
        assert self.turn in {'white', 'black'}
        if self.turn == 'white':
            self.turn = 'black'
            #print('Black to move.')
        else: #self.turn = 'black'
            self.turn = 'white'
            #print('White to move.')
    def score(self):
        assert self.turn in {'white', 'black'}
        score = 0
        if self.turn == 'white':
            for ch in self.board:
                if ch == 'r':
                    score -= 5
                elif ch == 'n' or ch == 'b':
                    score -= 3
                elif ch == 'q':
                    score -= 9
                elif ch == 'p':
                    score -= 1
                elif ch == 'R':
                    score += 5
                elif ch == 'N' or ch == 'B':
                    score += 3
                elif ch == 'Q':
                    score += 9
                elif ch == 'P':
                    score += 1
                elif ch == 'k':
                    score -= 1000000
                elif ch == 'K':
                    score += 1000000
            return score
        else: #self.turn == 'black':
            for ch in self.board:
                if ch == 'r':
                    score += 5
                elif ch == 'n' or ch == 'b':
                    score += 3
                elif ch == 'q':
                    score += 9
                elif ch == 'p':
                    score += 1
                elif ch == 'R':
                    score -= 5
                elif ch == 'N' or ch == 'B':
                    score -= 3
                elif ch == 'Q':
                    score -= 9
                elif ch == 'P':
                    score -= 1
                elif ch == 'k':
                    score += 1000000
                elif ch == 'K':
                    score -= 1000000
            return score
    def in_check(self):
        '''Checks whether its own king is in check in the current board state self.board.
        For example, if self.turn = 'white', checks to see if 'K' is still on the board after an extension on black's turn.
        '''
        assert self.turn in {'white', 'black'}
        check = False
        index = 0
        if self.turn == 'white':
            self.turn = 'black'
            board_list = self.extensions()
            while check == False and index < len(board_list):
                if 'K' not in board_list[index]:
                    check = True
                index += 1
            self.turn = 'white'
            return check
        else: #self.turn == 'black':
            self.turn = 'white'
            board_list = self.extensions()
            while check == False and index < len(board_list):
                if 'k' not in board_list[index]:
                    check = True
                index += 1
            self.turn = 'black'
            return check
    def checkmate(self):
        '''If all extensions of current board self.board have no King in them, it's checkmate.'''
        assert self.turn in {'white', 'black'}
        checkmate = True
        future_board = self.all_extensions()
        for board in future_board:
            if not board.in_check(): #if this future board makes the King not in check, there exist this possible extension to avoid checkmate
                checkmate = False
        return checkmate
    def stalemate(self):
        '''Returns True if there are no more possible extensions'''
        return len(self.all_extensions()) == 0
    def all_extensions(self):
        return self.extensions() + self.king_extensions()
    def extensions(self):
        '''Return list of highest scoring extensions of self.board. Omits extensions of the King.
        @type self: Board
        @type self.turn: list
        @rtype: list[list]'''
        assert self.turn in {'white', 'black'}
        list_extensions = []
        temp_board = self.board[:]
        if self.turn == 'white':
            for i in range(len(self.board)):
                if self.board[i] == 'P': #if character is a white Pawn
                    if self.board[i-8] == '-': #Pawn single jump
                        temp_board[i], temp_board[i-8] = '-', 'P'
                        if 0 <= i-8 <= 7: #if Pawn reaches end of the board
                            possible_promotions = ['R', 'N', 'B', 'Q']
                            for piece in possible_promotions:
                                temp_board[i-8] = piece
                                list_extensions.append(temp_board[:])
                            temp_board = self.board[:]
                        else:    
                            list_extensions.append(temp_board)
                            temp_board = self.board[:]
                            
                    if 48 <= i <= 55 and self.board[i-16] == '-' and self.board[i-8] == '-': #Pawn double jump
                        temp_board[i], temp_board[i-16] = '-', 'P'                       
                        list_extensions.append(temp_board)
                        temp_board = self.board[:]
                    if 0 <= i%8 <= 6 and self.board[i-7].islower(): #Pawn diagonal right take
                        temp_board[i], temp_board[i-7] = '-', 'P'
                        if 0 <= i-7 <= 7: #if Pawn reaches end of the board
                            possible_promotions = ['R', 'N', 'B', 'Q']
                            for piece in possible_promotions:
                                temp_board[i-7] = piece
                                list_extensions.append(temp_board[:])
                            temp_board = self.board[:]
                        else:    
                            list_extensions.append(temp_board)
                            temp_board = self.board[:]
                    if 1 <= i%8 <= 7 and self.board[i-9].islower(): #Pawn diagonal left take
                        temp_board[i], temp_board[i-9] = '-', 'P'
                        if 0 <= i-9 <= 7: #if Pawn reaches end of the board
                            possible_promotions = ['R', 'N', 'B', 'Q']
                            for piece in possible_promotions:
                                temp_board[i-9] = piece
                                list_extensions.append(temp_board[:])
                            temp_board = self.board[:]
                        else:    
                            list_extensions.append(temp_board)
                            temp_board = self.board[:]
                if self.board[i] in {'Q', 'B', 'R'}:
                    if self.board[i] in {'Q', 'R'}: #if character is a white Queen or Rook
                        temp_index = i
                        while temp_index >= 8 and not self.board[temp_index-8].isupper() and not self.board[temp_index].islower(): #check vertical up
                            temp_board[i], temp_board[temp_index-8] = '-', self.board[i]
                            temp_index -= 8
                            list_extensions.append(temp_board)
                            temp_board = self.board[:]
                        temp_index = i
                        while temp_index < 56 and not self.board[temp_index+8].isupper() and not self.board[temp_index].islower(): #check vertical down
                            temp_board[i], temp_board[temp_index+8] = '-', self.board[i]
                            temp_index += 8
                            list_extensions.append(temp_board)
                            temp_board = self.board[:]
                        temp_index = i
                        while temp_index % 8 != 7 and not self.board[temp_index+1].isupper() and not self.board[temp_index].islower(): #check horizontal right
                            temp_board[i], temp_board[temp_index+1] = '-', self.board[i]
                            temp_index += 1
                            list_extensions.append(temp_board)
                            temp_board = self.board[:]
                        temp_index = i
                        while temp_index % 8 != 0 and not self.board[temp_index-1].isupper() and not self.board[temp_index].islower(): #check horizontal right
                            temp_board[i], temp_board[temp_index-1] = '-', self.board[i]
                            temp_index -= 1
                            list_extensions.append(temp_board)
                            temp_board = self.board[:]
                    if self.board[i] in {'Q', 'B'}: #if character is a white Queen or Bishop
                        temp_index = i
                        while temp_index >= 8 and temp_index % 8 != 0 and not self.board[temp_index-9].isupper() and not self.board[temp_index].islower(): #check up left
                            temp_board[i], temp_board[temp_index-9] = '-', self.board[i]
                            temp_index -= 9
                            list_extensions.append(temp_board)
                            temp_board = self.board[:]
                        temp_index = i
                        while temp_index >= 8 and temp_index % 8 != 7 and not self.board[temp_index-7].isupper() and not self.board[temp_index].islower(): #check up right
                            temp_board[i], temp_board[temp_index-7] = '-', self.board[i]
                            temp_index -= 7
                            list_extensions.append(temp_board)
                            temp_board = self.board[:]
                        temp_index = i
                        while temp_index < 56 and temp_index % 8 != 0 and not self.board[temp_index+7].isupper() and not self.board[temp_index].islower(): #check bottom left
                            temp_board[i], temp_board[temp_index+7] = '-', self.board[i]
                            temp_index += 7
                            list_extensions.append(temp_board)
                            temp_board = self.board[:]
                        temp_index = i
                        while temp_index < 56 and temp_index % 8 != 7 and not self.board[temp_index+9].isupper() and not self.board[temp_index].islower(): #check bottom right
                            temp_board[i], temp_board[temp_index+9] = '-', self.board[i]
                            temp_index += 9
                            list_extensions.append(temp_board)
                            temp_board = self.board[:]
                if self.board[i] == 'N': #if character is a white Knight
                    if 0 <= i%8 <= 6: #right1
                        if i >= 16 and not self.board[i-15].isupper(): #right1up2
                            temp_board[i], temp_board[i-15] = '-', 'N'
                            list_extensions.append(temp_board)
                            temp_board = self.board[:]
                        if i < 48 and not self.board[i+17].isupper(): #right1down2
                            temp_board[i], temp_board[i+17] = '-', 'N'
                            list_extensions.append(temp_board)
                            temp_board = self.board[:]
                        if 0 <= i%8 <= 5: #right2
                            if i < 56 and not self.board[i+10].isupper(): #right2down1
                                temp_board[i], temp_board[i+10] = '-', 'N'
                                list_extensions.append(temp_board)
                                temp_board = self.board[:]
                            if i >= 8 and not self.board[i-6].isupper(): #right2up1
                                temp_board[i], temp_board[i-6] = '-', 'N'
                                list_extensions.append(temp_board)
                                temp_board = self.board[:]
                    if 1 <= i%8 <= 7: #left1
                        if i >= 16 and not self.board[i-17].isupper(): #left1up2
                            temp_board[i], temp_board[i-17] = '-', 'N'
                            list_extensions.append(temp_board)
                            temp_board = self.board[:]
                        if i < 48 and not self.board[i+15].isupper(): #left1down2
                            temp_board[i], temp_board[i+15] = '-', 'N'
                            list_extensions.append(temp_board)
                            temp_board = self.board[:]
                        if 2 <= i%8 <= 7: #left2
                            if i < 56 and not self.board[i+6].isupper(): #left2down1
                                temp_board[i], temp_board[i+6] = '-', 'N'
                                list_extensions.append(temp_board)
                                temp_board = self.board[:]
                            if i >= 8 and not self.board[i-10].isupper(): #left2up1
                                temp_board[i], temp_board[i-10] = '-', 'N'
                                list_extensions.append(temp_board)
                                temp_board = self.board[:]
                #if self.board[i] == 'K': #if character is a white King
                #    list_extensions += self.king_extensions(i)




        else: #if self.turn == 'black'
            for i in range(len(self.board)):
                if self.board[i] == 'p': #if character is a black Pawn
                    if self.board[i+8] == '-': #Pawn single jump
                        temp_board[i], temp_board[i+8] = '-', 'p'
                        if 56 <= i+8 <= 63: #if Pawn reaches end of the board
                            possible_promotions = ['r', 'n', 'b', 'q']
                            for piece in possible_promotions:
                                temp_board[i+8] = piece
                                list_extensions.append(temp_board[:])
                            temp_board = self.board[:]
                        else:
                            list_extensions.append(temp_board)
                            temp_board = self.board[:]
                    if 8 <= i <= 15 and self.board[i+16] == '-' and self.board[i+8] == '-': #Pawn double jump
                        temp_board[i], temp_board[i+16] = '-', 'p'                       
                        list_extensions.append(temp_board)
                        temp_board = self.board[:]
                    if 0 <= i%8 <= 6 and self.board[i+9].isupper(): #Pawn diagonal right take
                        temp_board[i], temp_board[i+9] = '-', 'p'
                        if 56 <= i+9 <= 63: #if Pawn reaches end of the board
                            possible_promotions = ['r', 'n', 'b', 'q']
                            for piece in possible_promotions:
                                temp_board[i+9] = piece
                                list_extensions.append(temp_board[:])
                            temp_board = self.board[:]
                        else:
                            list_extensions.append(temp_board)
                            temp_board = self.board[:]
                    if 1 <= i%8 <= 7 and self.board[i+7].isupper(): #Pawn diagonal left take
                        temp_board[i], temp_board[i+7] = '-', 'p'
                        if 56 <= i+7 <= 63: #if Pawn reaches end of the board
                            possible_promotions = ['r', 'n', 'b', 'q']
                            for piece in possible_promotions:
                                temp_board[i+7] = piece
                                list_extensions.append(temp_board[:])
                            temp_board = self.board[:]
                        else:
                            list_extensions.append(temp_board)
                            temp_board = self.board[:]
                if self.board[i] in {'q', 'b', 'r'}:
                    if self.board[i] in {'q', 'r'}: #if character is a black Queen or Rook
                        temp_index = i
                        while temp_index >= 8 and not self.board[temp_index-8].islower() and not self.board[temp_index].islower(): #check vertical up
                            temp_board[i], temp_board[temp_index-8] = '-', self.board[i]
                            temp_index -= 8
                            list_extensions.append(temp_board)
                            temp_board = self.board[:]
                        temp_index = i
                        while temp_index < 56 and not self.board[temp_index+8].islower() and not self.board[temp_index].islower(): #check vertical down
                            temp_board[i], temp_board[temp_index+8] = '-', self.board[i]
                            temp_index += 8
                            list_extensions.append(temp_board)
                            temp_board = self.board[:]
                        temp_index = i
                        while temp_index % 8 != 7 and not self.board[temp_index+1].islower() and not self.board[temp_index].islower(): #check horizontal right
                            temp_board[i], temp_board[temp_index+1] = '-', self.board[i]
                            temp_index += 1
                            list_extensions.append(temp_board)
                            temp_board = self.board[:]
                        temp_index = i
                        while temp_index % 8 != 0 and not self.board[temp_index-1].islower() and not self.board[temp_index].islower(): #check horizontal right
                            temp_board[i], temp_board[temp_index-1] = '-', self.board[i]
                            temp_index -= 1
                            list_extensions.append(temp_board)
                            temp_board = self.board[:]
                    if self.board[i] in {'q', 'b'}: #if character is a black Queen or Bishop
                        temp_index = i
                        while temp_index >= 8 and temp_index % 8 != 0 and not self.board[temp_index-9].islower() and not self.board[temp_index].islower(): #check up left
                            temp_board[i], temp_board[temp_index-9] = '-', self.board[i]
                            temp_index -= 9
                            list_extensions.append(temp_board)
                            temp_board = self.board[:]
                        temp_index = i
                        while temp_index >= 8 and temp_index % 8 != 7 and not self.board[temp_index-7].islower() and not self.board[temp_index].islower(): #check up right
                            temp_board[i], temp_board[temp_index-7] = '-', self.board[i]
                            temp_index -= 7
                            list_extensions.append(temp_board)
                            temp_board = self.board[:]
                        temp_index = i
                        while temp_index < 56 and temp_index % 8 != 0 and not self.board[temp_index+7].islower() and not self.board[temp_index].islower(): #check bottom left
                            temp_board[i], temp_board[temp_index+7] = '-', self.board[i]
                            temp_index += 7
                            list_extensions.append(temp_board)
                            temp_board = self.board[:]
                        temp_index = i
                        while temp_index < 56 and temp_index % 8 != 7 and not self.board[temp_index+9].islower() and not self.board[temp_index].islower(): #check bottom right
                            temp_board[i], temp_board[temp_index+9] = '-', self.board[i]
                            temp_index += 9
                            list_extensions.append(temp_board)
                            temp_board = self.board[:]
                if self.board[i] == 'n': #if character is a black Knight
                    if 0 <= i%8 <= 6: #right1
                        if i >= 16 and not self.board[i-15].islower(): #right1up2
                            temp_board[i], temp_board[i-15] = '-', 'n'
                            list_extensions.append(temp_board)
                            temp_board = self.board[:]
                        if i < 48 and not self.board[i+17].islower(): #right1down2
                            temp_board[i], temp_board[i+17] = '-', 'n'
                            list_extensions.append(temp_board)
                            temp_board = self.board[:]
                        if 0 <= i%8 <= 5: #right2
                            if i < 56 and not self.board[i+10].islower(): #right2down1
                                temp_board[i], temp_board[i+10] = '-', 'n'
                                list_extensions.append(temp_board)
                                temp_board = self.board[:]
                            if i >= 8 and not self.board[i-6].islower(): #right2up1
                                temp_board[i], temp_board[i-6] = '-', 'n'
                                list_extensions.append(temp_board)
                                temp_board = self.board[:]
                    if 1 <= i%8 <= 7: #left1
                        if i >= 16 and not self.board[i-17].islower(): #left1up2
                            temp_board[i], temp_board[i-17] = '-', 'n'
                            list_extensions.append(temp_board)
                            temp_board = self.board[:]
                        if i < 48 and not self.board[i+15].islower(): #left1down2
                            temp_board[i], temp_board[i+15] = '-', 'n'
                            list_extensions.append(temp_board)
                            temp_board = self.board[:]
                        if 2 <= i%8 <= 7: #left2
                            if i < 56 and not self.board[i+6].islower(): #left2down1
                                temp_board[i], temp_board[i+6] = '-', 'n'
                                list_extensions.append(temp_board)
                                temp_board = self.board[:]
                            if i >= 8 and not self.board[i-10].islower(): #left2up1
                                temp_board[i], temp_board[i-10] = '-', 'n'
                                list_extensions.append(temp_board)
                                temp_board = self.board[:]

                #if self.board[i] == 'k': #if character is a black King
                #    list_extensions += self.king_extensions(i)

        return list_extensions

    def king_extensions(self):
        #assert self.board[i] in {'K', 'k'}
        assert self.turn in {'white', 'black'}
        
        list_extensions = []
        temp_board = self.board[:]
        test_board = Board()
        test_board.turn = self.turn
        #because a king can never check another king anyways
        for i in range(len(self.board)):
            if self.board[i] == 'K' and self.turn == 'white': #if character is a white King
                if i%8 >= 1 and not self.board[i-1].isupper(): #left
                    temp_board[i], temp_board[i-1] = '-', 'K'
                    test_board.board = temp_board[:]
                    if not test_board.in_check():
                        list_extensions.append(temp_board)
                    temp_board = self.board[:]
                if i >= 8 and i%8 >= 1 and not self.board[i-9].isupper(): #left up
                    temp_board[i], temp_board[i-9] = '-', 'K'
                    test_board.board = temp_board[:]
                    if not test_board.in_check():
                        list_extensions.append(temp_board)
                    temp_board = self.board[:]
                if i < 56 and i%8 >= 1 and not self.board[i+7].isupper(): #left down
                    temp_board[i], temp_board[i+7] = '-', 'K'
                    test_board.board = temp_board[:]
                    if not test_board.in_check():
                        list_extensions.append(temp_board)
                    temp_board = self.board[:]
                if i%8 <= 6 and not self.board[i+1].isupper(): #right
                    temp_board[i], temp_board[i+1] = '-', 'K'
                    test_board.board = temp_board[:]
                    if not test_board.in_check():
                        list_extensions.append(temp_board)
                    temp_board = self.board[:]
                if i >= 8 and i%8 <= 6 and not self.board[i-7].isupper(): #right up
                    temp_board[i], temp_board[i-7] = '-', 'K'
                    test_board.board = temp_board[:]
                    if not test_board.in_check():
                        list_extensions.append(temp_board)
                    temp_board = self.board[:]
                if i < 56 and i%8 <= 6 and not self.board[i+9].isupper(): #right down
                    temp_board[i], temp_board[i+9] = '-', 'K'
                    test_board.board = temp_board[:]
                    if not test_board.in_check():
                        list_extensions.append(temp_board)
                    temp_board = self.board[:]
                if i >= 8 and not self.board[i-8].isupper(): #up
                    temp_board[i], temp_board[i-8] = '-', 'K'
                    test_board.board = temp_board[:]
                    if not test_board.in_check():
                        list_extensions.append(temp_board)
                    temp_board = self.board[:]
                if i < 56 and not self.board[i+8].isupper(): #down
                    temp_board[i], temp_board[i+8] = '-', 'K'
                    test_board.board = temp_board[:]
                    if not test_board.in_check():
                        list_extensions.append(temp_board)
                    temp_board = self.board[:]
                #check for Queen side castle
                if i == 60 and self.board[59] == '-' and self.board[58] == '-' and self.board[57] == '-' and self.board[56] == 'R' and self.castle_dict[56] == True and self.castle_dict[60] == True:
                    test_board.board = self.board[:]
                    if not test_board.in_check():
                        test_board.board[60], test_board.board[59] = '-', 'K',
                        if not test_board.in_check():
                            test_board.board[59], test_board.board[58], test_board.board[56] = 'R', 'K', '-'
                            if not test_board.in_check():
                                list_extensions.append(test_board.board)
                #check for King side castle
                if i == 60 and self.board[61] == '-' and self.board[62] == '-' and  self.board[63] == 'R' and self.castle_dict[60] == True and self.castle_dict[63] == True:
                    test_board.board = self.board[:]
                    if not test_board.in_check():
                        test_board.board[60], test_board.board[61] = '-', 'K'
                        if not test_board.in_check():
                            test_board.board[61], test_board.board[62], test_board.board[63] = 'R', 'K', '-'
                            if not test_board.in_check():
                                list_extensions.append(test_board.board)
                return list_extensions
            
            elif self.board[i] == 'k' and self.turn == 'black':
                #if character is a black King
                if i%8 >= 1 and not self.board[i-1].islower(): #left
                    temp_board[i], temp_board[i-1] = '-', 'k'
                    test_board.board = temp_board[:]
                    if not test_board.in_check():
                        list_extensions.append(temp_board)
                    temp_board = self.board[:]
                if i >= 8 and i%8 >= 1 and not self.board[i-9].islower(): #left up
                    temp_board[i], temp_board[i-9] = '-', 'k'
                    test_board.board = temp_board[:]
                    if not test_board.in_check():
                        list_extensions.append(temp_board)
                    temp_board = self.board[:]
                if i < 56 and i%8 >= 1 and not self.board[i+7].islower(): #left down
                    temp_board[i], temp_board[i+7] = '-', 'k'
                    test_board.board = temp_board[:]
                    if not test_board.in_check():
                        list_extensions.append(temp_board)
                    temp_board = self.board[:]
                if i%8 <= 6 and not self.board[i+1].islower(): #right
                    temp_board[i], temp_board[i+1] = '-', 'k'
                    test_board.board = temp_board[:]
                    if not test_board.in_check():
                        list_extensions.append(temp_board)
                    temp_board = self.board[:]
                if i >= 8 and i%8 <= 6 and not self.board[i-7].islower(): #right up
                    temp_board[i], temp_board[i-7] = '-', 'k'
                    test_board.board = temp_board[:]
                    if not test_board.in_check():
                        list_extensions.append(temp_board)
                    temp_board = self.board[:]
                if i < 56 and i%8 <= 6 and not self.board[i+9].islower(): #right down
                    temp_board[i], temp_board[i+9] = '-', 'k'
                    test_board.board = temp_board[:]
                    if not test_board.in_check():
                        list_extensions.append(temp_board)
                    temp_board = self.board[:]
                if i >= 8 and not self.board[i-8].islower(): #up
                    temp_board[i], temp_board[i-8] = '-', 'k'
                    test_board.board = temp_board[:]
                    if not test_board.in_check():
                        list_extensions.append(temp_board)
                    temp_board = self.board[:]
                if i < 56 and not self.board[i+8].islower(): #down
                    temp_board[i], temp_board[i+8] = '-', 'k'
                    test_board.board = temp_board[:]
                    if not test_board.in_check():
                        list_extensions.append(temp_board)
                    temp_board = self.board[:]
                #check for Queen side castle
                if i == 4 and self.board[3] == '-' and self.board[2] == '-' and self.board[1] == '-' and self.board[0] == 'r' and self.castle_dict[0] == True and self.castle_dict[4] == True:
                    test_board.board = self.board[:]
                    if not test_board.in_check():
                        test_board.board[4], test_board.board[3] = '-', 'k',
                        if not test_board.in_check():
                            test_board.board[3], test_board.board[2], test_board.board[0] = 'r', 'k', '-'
                            if not test_board.in_check():
                                list_extensions.append(test_board.board)
                #check for King side castle
                if i == 4 and self.board[5] == '-' and self.board[6] == '-' and  self.board[7] == 'r' and self.castle_dict[4] == True and self.castle_dict[7] == True:
                    test_board.board = self.board[:]
                    if not test_board.in_check():
                        test_board.board[4], test_board.board[5] = '-', 'k'
                        if not test_board.in_check():
                            test_board.board[5], test_board.board[6], test_board.board[7] = 'r', 'k', '-'
                            if not test_board.in_check():
                                list_extensions.append(test_board.board)
                return list_extensions

        return list_extensions                
        #King castle
        #King stalemate
        #King in check

    def move_event(self, new_board):
        '''Updates board self.board to new_board after a move is decided.
        Changes self.turn to the next turn.
        Checks to see if the King or Rooks have been moved and updates the dictionary self.castle_dict if they have been moved.
        @type new_board: list[list]
        @rtype: None
        '''
        for key in self.castle_dict:
            if self.castle_dict[key] == True:
                if new_board[key] == '-':
                    self.castle_dict[key] = False
                    
        self.board = new_board
        self.next_turn()
        if self.in_check():
            if self.checkmate():
                print('Checkmate!')
            else:
                print('Check!')
        if self.turn == 'white':
            print('White to move.')
        elif self.turn == 'black':
            print('Black to move.')

    def translate(self, coordinate):
        '''Translates a coordinate into the corresponding index in self.board.
        @type coordinate: str
        @rtype: int'''
        assert len(coordinate) == 2
        assert coordinate[0].isalpha()
        assert coordinate[1].isnumeric()
        alphabet = ['a', 'b', 'c' ,'d', 'e', 'f' ,'g' ,'h']
        return 8*(8-int(coordinate[1])) + alphabet.index(coordinate[0].lower())
    def notation_move(self, command):
        '''Moves a piece according to command. Intended for human player use.
        command in format 'start_coordinate end_coordinate', with any amount of spaces leading, inbetween or at rear end.
        Return updated board self.board.
        @type command: str
        @rtype: str
        '''
        new_command = command.replace(' ', '')
        assert len(new_command) == 4
        assert new_command[0].isalpha()
        assert new_command[2].isalpha()
        assert new_command[1].isnumeric()
        assert new_command[3].isnumeric()
        start_index = translate(new_command[:2])
        end_index = translate(new_command[2:])

        new_board = self.board[:]
        if self.turn == 'white':
            if self.board[start_index] == 'P' and 0 <= end_index <= 7:
                promote = input('What would you like to promote your Pawn to? ')
                while promote not in {'R', 'N', 'B', 'Q'}:
                    promote = input('Invalid choice, please pick from: R, N, B, or Q. ')
                    new_board[end_index] = promote
                    new_board[start_index] = '-'
                    if new_board in self.all_extensions():
                        return new_board
                    else:
                        new_command = input('Illegal move. Please input a new move. ')
                        return notation_move(new_command)
            if self.board[start_index] == 'K' and start_index == 60 and end_index == 58:
                if self.castle_dict[60] == True and self.castle_dict[56] == True and self.board[57] == '-' and self.board[58] == '-' and self.board[59] == '-': #Queenside castle
                    new_board[end_index] = 'K'
                    new_board[start_index] = '-'
                    new_board[56] = '-'
                    new_board[end_index+1] = 'R'
                    if new_board in self.all_extensions():
                        self.castle_dict[60] = False
                        return new_board
                    else:
                        new_command = input('Illegal move. Please input a new move. ')
                        return notation_move(new_command)
                else:
                    new_command = input('Illegal move. Cannot Castle. Please input a new move. ')
                    return notation_move(new_command)
            if self.board[start_index] == 'K' and start_index == 60 and end_index == 62:
                if self.castle_dict[60] == True and self.castle_dict[63] == True and self.board[61] == '-' and self.board[62] == '-': #Kingside castle
                    new_board[end_index] = 'K'
                    new_board[start_index] = '-'
                    new_board[63] = '-'
                    new_board[end_index-1] = 'R'
                    if new_board in self.all_extensions():
                        self.castle_dict[60] = False
                        return new_board
                    else:
                        new_command = input('Illegal move. Please input a new move. ')
                        return notation_move(new_command)
                else:
                    new_command = input('Illegal move. Cannot Castle. Please input a new move. ')
                    return notation_move(new_command)
                    
        if self.turn == 'black':
            if self.board[start_index] == 'p' and 56 <= end_index <= 63:
                promote = input('What would you like to promote your Pawn to? ')
                while promote not in {'r', 'n', 'b', 'q'}:
                    promote = input('Invalid choice, please pick from: r, n, b, or q. ')
                    new_board[end_index] = promote
                    new_board[start_index] = '-'
                    if new_board in self.all_extensions():
                        return new_board
                    else:
                        new_command = input('Illegal move. Please input a new move. ')
                        return notation_move(new_command)
            if self.board[start_index] == 'k' and start_index == 4 and end_index == 2:
                if self.castle_dict[4] == True and self.castle_dict[0] == True and self.board[1] == '-' and self.board[2] == '-' and self.board[3] == '-': #Queenside castle
                    new_board[end_index] = 'k'
                    new_board[start_index] = '-'
                    new_board[56] = '-'
                    new_board[end_index+1] = 'r'
                    if new_board in self.all_extensions():
                        self.castle_dict[4] = False
                        return new_board
                    else:
                        new_command = input('Illegal move. Please input a new move. ')
                        return notation_move(new_command)
                else:
                    new_command = input('Illegal move. Cannot Castle. Please input a new move. ')
                    return notation_move(new_command)
            if self.board[start_index] == 'k' and start_index == 4 and end_index == 6:
                if self.castle_dict[4] == True and self.castle_dict[7] == True and self.board[5] == '-' and self.board[6] == '-': #Kingside castle
                    new_board[end_index] = 'k'
                    new_board[start_index] = '-'
                    new_board[63] = '-'
                    new_board[end_index-1] = 'r'
                    if new_board in self.all_extensions():
                        self.castle_dict[4] = False
                        return new_board
                    else:
                        new_command = input('Illegal move. Please input a new move. ')
                        return notation_move(new_command)
                else:
                    new_command = input('Illegal move. Cannot Castle. Please input a new move. ')
                    return notation_move(new_command)
        else: #every other move that doesn't involve King castling or Pawn promotion
            piece_to_move = new_board[start_index][:]
            new_board[end_index] = piece_to_move
            new_board[start_index] = '-'
            if new_board in self.all_extensions():
                if self.turn == 'white':
                    if piece_to_move == 'K' and start_index == 60:
                        self.castle_dict[60] = False
                    if piece_to_move == 'R':
                        if start_index == 56:
                            self.castle_dict[56] = False
                        if start_index == 63:
                            self.castle_dict[63] = False
                else: #self.turn == 'black':
                    if piece_to_move == 'k' and start_index == 4:
                        self.castle_dict[4] = False
                    if piece_to_move == 'r':
                        if start_index == 0:
                            self.castle_dict[0] = False
                        if start_index == 7:
                            self.castle_dict[7] = False
                return new_board
            else:
                new_command = input('Illegal move. Please input a new move. ')
                return notation_move(new_command)

        

        


if __name__ == '__main__YO':
    def test_board(test_piece, surround='-', centre=35):
        '''Returns a list of str representative of a board with test_piece in the centre surrounded on all 9 spaces by the surround piece
        @type test_piece, surround: str
        @rtype list[str]'''
        assert centre
        board = ['-']*64
        board[centre] = test_piece
        board[centre-9], board[centre-8], board[centre-7], board[centre-1], board[centre+1], board[centre+7], board[centre+8], board[centre+9] = surround, surround, surround, surround, surround, surround, surround, surround
        return board
    b = Board()
    b.fill_board()
    b.start_game()
    b.next_turn()

    #regular board
    #b.board = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']

    #castle board
    #b.board = ['r', '-', '-', '-', 'k', '-', '-', 'r', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'N', 'B', 'Q', '-', 'B', 'N', '-', 'R', '-', '-', '-', 'K', '-', '-', 'R']

    #b.board = test_board('K', 'p')
    b.board = ['-']*50 + ['p'] + ['-']*7 + ['Q'] + ['-']*5
    
    a = Board()
    a.turn = 'white'
    extensions = b.all_extensions()
    print('ORIGINAL')
    print(b)
    for i in range(len(extensions)):
        a.board = extensions[i]
        print(a)
        print(a.score())
