#Author: Christine Ito
#Github username: itochr
#Date: 8/10/23
#Description: final project- program a chess-inspired game whose goal is to get the king to row 8
#               without placing either king in check

class Board:
    """displays a visual representation of the chess board and pieces"""
    def __init__(self):
        self._zero=  ['   ',' a ',' b ',' c ',' d ',' e ',' f ',' g ',' h ']
        self._eight= [' 8 ','   ','   ','   ','   ','   ','   ','   ','   ']
        self._seven= [' 7 ','   ','   ','   ','   ','   ','   ','   ','   ']
        self._six=   [' 6 ','   ','   ','   ','   ','   ','   ','   ','   ']
        self._five=  [' 5 ','   ','   ','   ','   ','   ','   ','   ','   ']
        self._four=  [' 4 ','   ','   ','   ','   ','   ','   ','   ','   ']
        self._three= [' 3 ','   ','   ','   ','   ','   ','   ','   ','   ']
        self._two=   [' 2 ','wr','wb2','wk2','   ','   ','bk2','bb2','br']
        self._one=   [' 1 ','wk','wb1','wk1','   ','   ','bk1','bb1','bk']
        self._board = [self._zero, self._eight, self._seven, self._six, self._five, self._four,
                       self._three,self._two, self._one]

    def update_board(self, piece, start, end):
        """updates position of pieces after each move in visual representation of game board"""
        start_col= start[0]
        start_row= start[1]
        end_col= end[0]
        end_row= int(end[1])
        new_row= self._board[9-end_row]
        for row in self._board:         #delete piece from old position
            if piece in row:
                spot= row.index(piece)
                row[spot]= '   '
        for index in new_row:     #add piece to new position
            if end_col== 'a':
                new_row[1]= piece
            if end_col== 'b':
                new_row[2]= piece
            if end_col == 'c':
                new_row[3] = piece
            if end_col== 'd':
                new_row[4]= piece
            if end_col== 'e':
                new_row[5]= piece
            if end_col== 'f':
                new_row[6]= piece
            if end_col== 'g':
                new_row[7]= piece
            if end_col== 'h':
                new_row[8]= piece
        return self.get_board

    def get_board(self):
        """prints the board"""
        print(*self._board, sep='\n')

class ChessVar:
    """class that contains the rules for each type of piece, dictionary of current positions
     and capture rules"""
    def __init__(self):
        #self._board= Board.get_board
        self._positions= {'a2': 'wr', 'a1': 'wk',
                          'b2': 'wb2', 'b1': 'wb1',
                          'c2': 'wk2', 'c1': 'wk1',
                          'h2': 'br', 'h1': 'bk',
                          'g2': 'bb2', 'g1': 'bb1',
                          'f2': 'bk2', 'f1': 'bk1'}
        self._total_moves= 0
        self._capture= False
        self._game_state= 'UNFINISHED'
        self._white_eight= False

    def get_positions(self):
        """dictionary of current game piece positions"""
        return self._positions

    def whose_move(self):
        """keeps track of whose move it is"""
        if self._total_moves % 2 == 0:
            return "W"
        if self._total_moves %2 ==1:
            return "B"

    def get_game_state(self):
        """returns status of the game, who won, or if it was a tie"""
        bposition= [key for key in self._positions if self._positions[key] == 'bk']
        wposition = [key for key in self._positions if self._positions[key] == 'wk']
        if self._white_eight== False:
            if bposition[0][-1] == '8':
                self._game_state = 'BLACK_WON'
            if wposition[0][-1] == '8':
                self._white_eight= True
        if self._white_eight == True:
            if bposition[0][-1] == '8':
                self._game_state = 'TIE'
            else:
                self._game_state= 'WHITE_WON'
        return self._game_state


    def make_move(self, move1, move2):
        """moves the pieces and gives error to moves that break the rules"""
        start_col= move1[0]
        start_row= int(move1[1])
        end_col= move2[0]
        end_row= int(move2[1])
        piece= self._positions[move1]
        team= piece[0]

        if end_row > 8:
            return False
        if move1 not in self._positions:            #if there isn't a piece at starting point
            return False

        if self.whose_move() != team.upper():    #if player tries to move someone else's piece= Move not legal
            return False

        if self._game_state != 'UNFINISHED':
            return False

        #if move2 has a piece from own team, return False
        if move2 in self._positions:
            newspot= self._positions[move2]
            if newspot[0]== team:
                return False

            #rooks
        if piece == 'wr' or piece == 'br':
            if start_row == end_row or start_col == end_col:
                return self.replace_pieces(piece, move1, move2)
            else:
                return False

        #kings
        elif piece == 'wk' or piece == 'bk':
            if end_row == start_row:                #plus or minus column, but same row
                if end_col > chr(ord(start_col)+1):
                    return False
                if end_col < chr(ord(start_col)-1):
                    return False
                else:
                    return self.replace_pieces(piece, move1, move2)


            if end_col== start_col:                 #plus or minus row, but same column
                if end_row == start_row+1:
                    return self.replace_pieces(piece, move1, move2)
                if end_row== start_row-1:
                    return self.replace_pieces(piece, move1, move2)
            if (end_col == chr(ord(start_col) + 1)) and end_row == start_row + 1:  #all possible diagonal moves
                return self.replace_pieces(piece, move1, move2)
            if (end_col == chr(ord(start_col) - 1)) and end_row == start_row - 1:
                return self.replace_pieces(piece, move1, move2)
            if (end_col == chr(ord(start_col) + 1)) and end_row == start_row - 1:
                return self.replace_pieces(piece, move1, move2)
            if (end_col == chr(ord(start_col) - 1)) and end_row == start_row + 1:
                return self.replace_pieces(piece, move1, move2)
            else:
                return False

        #bishops
        elif piece == 'wb1' or piece == 'wb2' or piece == 'bb1' or piece == 'bb2':
            for num in range(0,7):
                if (end_row== start_row + num and end_col== chr(ord(start_col)+num)):
                    return self.replace_pieces(piece, move1, move2)
                if (end_row== start_row - num and end_col== chr(ord(start_col)+num)):
                    return self.replace_pieces(piece, move1, move2)
                if (end_row== start_row + num and end_col== chr(ord(start_col)-num)):
                    return self.replace_pieces(piece, move1, move2)
                if (end_row== start_row - num and end_col== chr(ord(start_col)-num)):
                    return self.replace_pieces(piece, move1, move2)
            else:
                return False

        #knights
        elif piece == 'wk1' or piece== 'wk2' or piece== 'bk1' or piece== 'bk2':
            if end_row == start_row + 1 and end_col == chr(ord(start_col)+2):
                return self.replace_pieces(piece, move1, move2)
            if end_row == start_row + 2 and end_col == chr(ord(start_col)+1):
                return self.replace_pieces(piece, move1, move2)
            if end_row == start_row + 1 and end_col == chr(ord(start_col)-2):
                return self.replace_pieces(piece, move1, move2)
            if end_row == start_row + 2 and end_col == chr(ord(start_col)-1):
                return self.replace_pieces(piece, move1, move2)
            if end_row == start_row - 1 and end_col == chr(ord(start_col)+2):
                return self.replace_pieces(piece, move1, move2)
            if end_row == start_row - 2 and end_col == chr(ord(start_col)-1):
                return self.replace_pieces(piece, move1, move2)
            if end_row == start_row - 1 and end_col == chr(ord(start_col)-2):
                return self.replace_pieces(piece, move1, move2)
            if end_row == start_row - 2 and end_col == chr(ord(start_col)-1):
                return self.replace_pieces(piece, move1, move2)
            else:
                return False
        return True


    def replace_pieces(self, piece, start, end):
        """if the move is legal, this method moves game piece from starting position to ending position,
        determines if a king is at row 8, and determines if there is a capture"""

        #determine if there is a possible capture
        self._total_moves += 1
        if end in self._positions:
            capturing_piece = self._positions[start]
            captured_piece = self._positions[end]
            self._capture== True

        team= piece[0]
        bking_pos= [key for key in self._positions if self._positions[key]== 'bk']
        wking_pos = [key for key in self._positions if self._positions[key] == 'wk']

            # players can put NEITHER king in check
            # search kings' positions as end moves to determine if any are legal for each player
        if team== 'w':
            #white team is moving- is either king in check?
            check_bking= self.check_legal(piece, end, bking_pos[0])
            if check_bking== True:
                return False
            for player in self._positions.values():
                check_piece = [key for key, val in self._positions.items() if val == player]
                if player[0]== 'b' and player != 'bk':         #check black players to see if a white move puts wking in check
                    is_wking_in_check = self.check_legal(player, check_piece[0], wking_pos[0])
                    if is_wking_in_check == True:
                        self._total_moves -= 1
                        return False
                    else:
                        #if neither king is at risk of being checked
                        if piece== 'wk' and end[1]=='8':
                            self._white_eight= True
                        replace = self._positions[start]
                        del self._positions[start]
                        self._positions[end] = replace
                        if self._capture== True:
                            return capture_check(capturing_piece, captured_piece)
                        return True

                if player[0]== 'w' and player != 'wk':
                    is_bking_in_check = self.check_legal(player, check_piece[0], bking_pos[0])
                    if is_bking_in_check == True:
                        self._total_moves -= 1
                        return False
                    else:
                        #if neither king is at risk of being checked
                        if piece== 'wk' and end[1]=='8':
                            self._white_eight= True
                        replace = self._positions[start]
                        del self._positions[start]
                        self._positions[end] = replace
                        if self._capture== True:
                            return capture_check(capturing_piece, captured_piece)
                            return True
                        else:
                            return True

        if team == 'b':
            # black team is moving- are either kings in check?
            check_wking= self.check_legal(piece, end, wking_pos[0])
            if check_wking== True:
                self._total_moves -= 1
                return False
            for player in self._positions.values():
                check_piece = [key for key, val in self._positions.items() if val == player]
                if player[0] == 'w' and player != 'wk':            # check white players to see if a black move puts bking in check
                    is_bking_in_check = self.check_legal(player, check_piece[0], bking_pos[0])
                    if is_bking_in_check == True:
                        self._total_moves -= 1
                        return False
                    else:
                        # if neither king is at risk of being checked
                        replace = self._positions[start]
                        del self._positions[start]
                        self._positions[end] = replace
                        if self._capture == True:
                            return capture_check(capturing_piece, captured_piece)
                            return True
                        else:
                            return True
                if player[0] == 'b' and player != 'bk':
                    is_wking_in_check = self.check_legal(player, check_piece[0], wking_pos[0])
                    if is_wking_in_check == True:
                        self._total_moves -= 1
                        return False
                    else:
                        # if neither king is at risk of being checked
                        replace = self._positions[start]
                        del self._positions[start]
                        self._positions[end] = replace
                        if self._capture == True:
                            return capture_check(capturing_piece, captured_piece)
                        return True


    def capture_check(self, capturing, captured):
        """when a piece lands on a square containing another piece, this method determines if capture is legal
        and if it is, deletes captured piece from dictionary"""
        capturing_team= capturing[0]
        captured_team= captured[0]
        if capturing_team != captured_team:
            find_coord = [key for key, val in self._positions.items() if val == captured]
            del self._positions[find_coord]
            self._capture= False
        else:
            self._total_moves-=1


    def check_legal(self, piece, move1, move2):
        """receives parameters from replace_pieces to determine if a move places own king in check.
        If so, move does not happen"""
        start_col= move1[0]
        start_row= int(move1[1])
        end_col= move2[0]
        end_row= int(move2[1])
        team= piece[0]

            #rooks
        if piece == 'wr' or piece == 'br':
            if start_row == end_row:
                #search positions dict for other players in that row/column between rook and king
                for item in self._positions:
                    if self._positions[item] != 'bk' or 'wk' or piece:
                        if item[0] == end_row:
                            if item[1] >= end_row and item[1] < start_row:        #is it between rook and king in that col?
                                return False
                            if item[1] <= end_row and item[1] > start_row:
                                return False
                        else:
                            return True
            if start_col == end_col:
                for item in self._positions:
                    if self._positions[item] != 'bk' or 'wk':
                        if item[0] == end_col:
                            if item[1] >= end_col and item[1] < start_col:        #is it between rook and king in that col?
                                return False
                            if item[1] <= end_col and item[1] > start_col:
                                return False
                        else:
                            return True
            else:
                return False

        #kings
        #if kings are one square away from each other, they are in check
        if piece == 'wk' or piece == 'bk':
            if end_row == start_row:
                if end_col == chr(ord(start_col) + 1) or end_col == chr(ord(start_col) -1):
                    return True
            if end_col == start_col:
                if abs(end_row-start_row) <= 1:
                    return True

        #bishops
        if piece == 'wb1' or piece == 'wb2' or piece == 'bb1' or piece == 'bb2':
            for num in range(0,7):
                if (end_row== start_row + num and end_col== chr(ord(start_col)+num)):
                    return True
                if (end_row== start_row - num and end_col== chr(ord(start_col)+num)):
                    return True
                if (end_row== start_row + num and end_col== chr(ord(start_col)-num)):
                    return True
                if (end_row== start_row - num and end_col== chr(ord(start_col)-num)):
                    return True
            else:
                return False

        if piece == 'wk1' or piece== 'wk2' or piece== 'bk1' or piece== 'bk2':
            if end_row == start_row + 1 and end_col == chr(ord(start_col) + 2):
                return True
            if end_row == start_row + 2 and end_col == chr(ord(start_col) + 1):
                return True
            if end_row == start_row + 1 and end_col == chr(ord(start_col) + 2):
                return True
            if end_row == start_row + 2 and end_col == chr(ord(start_col) - 1):
                return True
            if end_row == start_row - 1 and end_col == chr(ord(start_col) + 2):
                return True
            if end_row == start_row - 2 and end_col == chr(ord(start_col) - 1):
                return True
            if end_row == start_row - 1 and end_col == chr(ord(start_col) - 2):
                return True
            if end_row == start_row - 2 and end_col == chr(ord(start_col) - 1):
                return True
            else:
                return False

    def print_board(self, piece, start, end):
        """calls Board class to update game piece positions on board visual"""
        return Board.update_board(piece, start, end)



def main():
    """main function for code testing"""
    myBoard= Board()
    myGame= ChessVar()

    myGame.make_move('a2', 'a5')        #white
    myBoard.update_board('wr', 'a2', 'a5')

    myGame.make_move('g2', 'd5')        #black
    myBoard.update_board('bb2', 'g2', 'd5')

    myGame.make_move('a1', 'a2')        #white
    myBoard.update_board('wk', 'a1', 'a2')

    # myGame.make_move('f2', 'g4')        #black
    # myBoard.update_board('bk2', 'f2', 'g4')

    # myGame.make_move('a2', 'a3')        # white
    # myBoard.update_board('wk', 'a2', 'a3')
    #
    # myGame.make_move('h2', 'h3')        # black- illegal move
    # myBoard.update_board('br', 'h2', 'h2')
    #
    # myGame.make_move('h2', 'h7')        # black
    # myBoard.update_board('br', 'h2', 'h7')
    #
    # myGame.make_move('c1', 'b3')        # white
    # myBoard.update_board('wk1', 'c1', 'b3')
    #
    # myGame.make_move('d5', 'b3')        # black
    # myBoard.update_board('bb2', 'd5', 'b3')

    # myGame.make_move('b1', 'a2')        # white
    # myBoard.update_board('wb1', 'b2', 'a2')
    #
    # myGame.make_move('f1', 'd2')       # black
    # myBoard.update_board('bk1', 'f1', 'd2')
    #
    # myGame.make_move('a2', 'e6')        # white
    # myBoard.update_board('wb1', 'a2', 'e6')

    # myGame.make_move('a7', 'b7')        # white
    # myBoard.update_board('wk', 'a7', 'a8')
    #
    # myGame.make_move('h7', 'h8')        # black
    # myBoard.update_board('bk', 'h7', 'h8')
    #
    print(myGame.get_game_state())
    print(myGame.get_positions())
    print(myGame.whose_move())
    print(*myBoard.get_board(), sep='\n')


if __name__== '__main__':
    main()


