import pygame
import sys
from itertools import groupby
import paths

#Display
WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('CHESS')
pygame.init()
pygame.font.init()

#Colours
black = (0, 0, 0)
white = (255, 255, 255)
orange = (255, 128, 10)
light_grey = (200, 200, 200)
dark_grey = (100, 100, 100)
light_blue = (129, 212, 250)
dark_blue = (1, 47, 75)
green = (10, 250, 50)
red = (250, 0, 30)
dark_brown = (142, 92, 71)
light_brown = (240, 217, 181)

bg_colour = black
string = '0abcdefgh'

sqr_size = 100
screen.fill(bg_colour)

# PIECES
b_pawn = [pygame.image.load('PIECES/b_pawn.png'), 'b_pawn']
b_bishop = [pygame.image.load('PIECES/b_bishop.png'), 'b_bishop']
b_knight = [pygame.image.load('PIECES/b_knight.png'), 'b_knight']
b_rook = [pygame.image.load('PIECES/b_rook.png'), 'b_rook']
b_queen = [pygame.image.load('PIECES/b_queen.png'), 'b_queen']
b_king = [pygame.image.load('PIECES/b_king.png'), 'b_king']

w_pawn = [pygame.image.load('PIECES/w_pawn.png'), 'w_pawn']
w_bishop = [pygame.image.load('PIECES/w_bishop.png'), 'w_bishop']
w_knight = [pygame.image.load('PIECES/w_knight.png'), 'w_knight']
w_rook = [pygame.image.load('PIECES/w_rook.png'), 'w_rook']
w_queen = [pygame.image.load('PIECES/w_queen.png'), 'w_queen']
w_king = [pygame.image.load('PIECES/w_king.png'), 'w_king']

#The inital setup of the board
initial_rows = [[b_rook, b_knight, b_bishop, b_queen, b_king, b_bishop, b_knight, b_rook], 
                [b_pawn for _ in range(8)], 0, 0, 0, 0, [w_pawn for _ in range(8)],
                [w_rook, w_knight, w_bishop, w_queen, w_king, w_bishop, w_knight, w_rook]]

pos_dic = {100 : 'a', 200 : 'b', 300 : 'c', 400 : 'd',
           500 : 'e', 600 : 'f', 700 : 'g', 800 : 'h'
           }

positions = [char + str(num) for num in range(8, 0, -1) for char in string[1:]]
kings_pos = {'w' : 'e1', 'b' : 'e8'}
board = {}
bishop_paths = paths.bishop()
knight_paths = paths.knight()
rook_paths = paths.rook()
queen_paths = paths.queen()
king_paths = paths.king()

out = paths.out

class Square:
    def __init__(self, x: int, y: int, colour: tuple):
        self.x = x
        self.y = y
        self.colour = colour
        self.letter = pos_dic[self.x]
        self.num = int(9 - self.y/100)
        self.occ = False
        self.piece = None
        self.piece_history = []
        self.pos = self.letter + str(self.num)

    def draw(self):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, sqr_size, sqr_size))


class Piece:
    def __init__(self, piece: tuple, num_of_moves=0):
        self.piece = piece[0]
        self.name = piece[1]
        self.prev_pos = None
        self.num_of_moves = num_of_moves
        
    def place(self, pos):
        self.letter = pos[0]
        self.num = int(pos[1])
        self.x = string.index(self.letter) * 100
        self.pos = pos
        self.curr_sqr = board[self.pos]
        x = string.index(self.letter) * 100
        y = 900 - 100 * self.num
        self.show = pygame.transform.scale(self.piece, (sqr_size - 20, sqr_size - 20))
        self.rect = self.piece.get_rect()
        self.rect = self.rect.move((x + 10, y + 10))
        screen.blit(self.show, self.rect)
        board[self.pos].occ = True
        board[self.pos].piece = self

    def dummy_place(self, pos):
        self.letter = pos[0]
        self.num = int(pos[1])
        self.x = string.index(self.letter) * 100
        self.pos = pos
        self.curr_sqr = board[self.pos]
        board[self.pos].occ = True
        board[self.pos].piece = self

    def av_moves(self):
        av_sqrs = []
        letter, num = self.letter, self.num
        name = self.name
        if name[2:] == 'pawn':
            av_sqrs = en_passant(self)
            if self.num_of_moves == 0:
                if name[0] == 'w':
                    if self.letter == 'a':
                        pos1, pos2, pos3 = 'a3', 'a4', 'b3'
                        if board[pos1].occ is False:
                            av_sqrs.append(pos1)
                            if board[pos2].occ is False:
                                av_sqrs.append(pos2)
                        if board[pos3].occ is True and board[pos3].piece.name[0] == 'b':
                            av_sqrs.append(pos3)
                    elif self.letter == 'h':
                        pos1, pos2, pos3 = 'h3', 'h4', 'g3'
                        if board[pos1].occ is False:
                            av_sqrs.append(pos1)
                            if board[pos2].occ is False:
                                av_sqrs.append(pos2)
                        if board[pos3].occ is True and board[pos3].piece.name[0] == 'b':
                            av_sqrs.append(pos3)
                    else:
                        pos1, pos2 = self.letter + '3', self.letter + '4'   
                        pos3, pos4 = pos_dic[self.x-100] + '3', pos_dic[self.x + 100] + '3'
                        if board[pos1].occ is False:
                            av_sqrs.append(pos1)
                            if board[pos2].occ is False:
                                av_sqrs.append(pos2)
                        if board[pos3].occ is True and board[pos3].piece.name[0] == 'b':
                            av_sqrs.append(pos3)
                        if board[pos4].occ is True and board[pos4].piece.name[0] == 'b':
                            av_sqrs.append(pos4)    
                else:
                    if self.letter == 'a':
                        pos1, pos2, pos3 = 'a6', 'a5', 'b6'
                        if board[pos1].occ is False:
                            av_sqrs.append(pos1)
                            if board[pos2].occ is False:
                                av_sqrs.append(pos2)
                        if board[pos3].occ is True and board[pos3].piece.name[0] == 'w':
                            av_sqrs.append(pos3)
                    elif self.letter == 'h':
                        pos1, pos2, pos3 = 'h6', 'h5', 'g6'
                        if board[pos1].occ is False:
                            av_sqrs.append(pos1)
                            if board[pos2].occ is False:
                                av_sqrs.append(pos2)
                        if board[pos3].occ is True and board[pos3].piece.name[0] == 'w':
                            av_sqrs.append(pos3)
                    else:
                        pos1, pos2 = self.letter + '6', self.letter + '5'   
                        pos3, pos4 = pos_dic[self.x-100] + '6', pos_dic[self.x + 100] + '6'
                        if board[pos1].occ is False:
                            av_sqrs.append(pos1)
                            if board[pos2].occ is False:
                                av_sqrs.append(pos2)
                        if board[pos3].occ is True and board[pos3].piece.name[0] == 'w':
                            av_sqrs.append(pos3)
                        if board[pos4].occ is True and board[pos4].piece.name[0] == 'w':
                            av_sqrs.append(pos4)
            else:
                if name[0] == 'w':
                    if letter == 'a':
                        take_right_pos = pos_dic[self.x + 100] + str(num + 1)
                        take_right = board[take_right_pos]
                        check_empty = letter + str(num+1)
                        if board[check_empty].occ is False:
                            av_pos1 = letter + str(num + 1) 
                            av_sqrs.append(av_pos1)
                        if take_right.occ is True:
                            if take_right.piece.name[0] == 'b':
                                av_sqrs.append(take_right.pos)
                    elif letter == 'h':
                        take_left_pos = pos_dic[self.x - 100] + str(num + 1)
                        take_left = board[take_left_pos]
                        check_empty = letter + str(num + 1)
                        if board[check_empty].occ is False:
                            av_pos1 = letter + str(num + 1) 
                            av_sqrs.append(av_pos1)
                        if take_left.occ is True:
                            if take_left.piece.name[0] == 'b':
                                av_sqrs.append(take_left.pos)
                    else:
                        take_left_pos = pos_dic[self.x - 100] + str(num + 1)
                        take_right_pos = pos_dic[self.x + 100] + str(num + 1)
                        take_left = board[take_left_pos]
                        take_right = board[take_right_pos]
                        check_empty = letter + str(num+1)
                        if board[check_empty].occ is False:
                            av_pos1 = letter + str(num + 1) 
                            av_sqrs.append(av_pos1)
                        if take_right.occ is True:
                            if take_right.piece.name[0] == 'b':
                                av_sqrs.append(take_right.pos)
                        if take_left.occ is True:
                            if take_left.piece.name[0] == 'b':
                                av_sqrs.append(take_left.pos)         
                else:
                    if letter == 'a':
                        take_right_pos = pos_dic[self.x + 100] + str(num - 1)
                        take_right = board[take_right_pos]
                        check_empty = letter + str(num - 1)
                        if board[check_empty].occ is False:
                            av_pos1 = letter + str(num - 1) 
                            av_sqrs.append(av_pos1)
                        if take_right.occ is True:
                            if take_right.piece.name[0] == 'w':
                                av_sqrs.append(take_right.pos)
                    elif letter == 'h':
                        take_left_pos = pos_dic[self.x - 100] + str(num - 1)
                        take_left = board[take_left_pos]
                        check_empty = letter + str(num - 1)
                        if board[check_empty].occ is False:
                            av_sqrs.append(check_empty)
                        if take_left.occ is True:
                            if take_left.piece.name[0] == 'w':
                                av_sqrs.append(take_left.pos)
                    else:
                        take_left_pos = pos_dic[self.x - 100] + str(num - 1)
                        take_right_pos = pos_dic[self.x + 100] + str(num - 1)
                        take_left = board[take_left_pos]
                        take_right = board[take_right_pos]
                        check_empty = letter + str(num - 1)
                        if board[check_empty].occ is False:
                            av_sqrs.append(check_empty)
                        if take_right.occ is True:
                            if take_right.piece.name[0] == 'w':
                                av_sqrs.append(take_right.pos)
                        if take_left.occ is True:
                            if take_left.piece.name[0] == 'w':
                                av_sqrs.append(take_left.pos)
        elif name[2:] == 'knight':
            sqrs = knight_paths[self.pos]
            for el in sqrs:
                sqr = board[el]
                if sqr.occ is False:
                    av_sqrs.append(el)
                else:
                    if sqr.piece.name[0] != self.name[0]:
                        av_sqrs.append(el)
                    else:
                        None 
        elif name[2:] == 'rook':
            sqrs = rook_paths[self.pos]
            bounds = [t for t in sqrs if out(t)]
            paths = [list(group) for k, group in groupby(sqrs, lambda x: x in bounds) if not k]
            for path in paths:
                for pos in path:
                    sqr = board[pos]
                    if sqr.occ is False:
                        av_sqrs.append(pos)
                    else:
                        if sqr.piece.name[0] != self.name[0]:
                            av_sqrs.append(pos)
                            if 'king' not in sqr.piece.name:
                                break
                            else:
                                None
                        else:
                            break
        elif name[2:] == 'bishop':
            sqrs = bishop_paths[self.pos]
            bounds = [t for t in sqrs if out(t)]
            paths = [list(group) for k, group in groupby(sqrs, lambda x: x in bounds) if not k]
            for path in paths:
                for pos in path:
                    sqr = board[pos]
                    if sqr.occ is False:
                        av_sqrs.append(pos)
                    else:
                        if sqr.piece.name[0] != self.name[0]:
                            av_sqrs.append(pos)
                            if 'king' not in sqr.piece.name:
                                break
                            else:
                                None
                        else:
                            break
        elif name[2:] == 'queen':
            sqrs = queen_paths[self.pos]
            bounds = [t for t in sqrs if out(t)]
            paths = [list(group) for k, group in groupby(sqrs, lambda x: x in bounds) if not k]
            for path in paths:
                for pos in path:
                    sqr = board[pos]
                    if sqr.occ is False:
                        av_sqrs.append(pos)
                    else:
                        if sqr.piece.name[0] != self.name[0]:
                            av_sqrs.append(pos)
                            if 'king' not in sqr.piece.name:
                                break
                            else:
                                None
                        else:
                            break
        elif name[2:] == 'king':
            if castle_king_side(self) is True:
                av_sqrs.append('g' + str(self.num))
            if castle_queen_side(self) is True:
                av_sqrs.append('c' + str(self.num))
            sqrs = king_paths[self.pos]
            if self.name[0] == 'w':
                for sqr in sqrs:
                    check = False
                    if sqr in black_range():
                        check = True 
                    if not check and board[sqr].occ is False:
                        av_sqrs.append(sqr)
                    elif not check and board[sqr].piece.name[0] == 'b':
                        av_sqrs.append(sqr)
                    else:
                        None
            else:
                for sqr in sqrs:
                    check = False
                    if sqr in white_range():
                        check = True 
                    if not check and board[sqr].occ is False:
                        av_sqrs.append(sqr)
                    elif not check and board[sqr].piece.name[0] == 'w':
                        av_sqrs.append(sqr)
        return av_sqrs

def draw_rect(colour: tuple, sqr: Square):
    '''
    Drawing a border around the kings square to indicate a check
    '''
    for i in range(4):
        pygame.draw.rect(screen, colour, (sqr.x+i,sqr.y+i,sqr_size-4,sqr_size-4), 1)
    pygame.display.update()
    return 

def find_black():
    '''
    Returns a list containing the positions of all the black pieces currently on the board
    '''
    global board
    lst = [key for key, value in board.items() if value.occ is True and value.piece.name[0] == 'b']
    return lst

def find_white():
    '''
    Returns a list containing the positions of all the white pieces currently on the board
    '''
    global board
    lst = [key for key, value in board.items() if value.occ is True and value.piece.name[0] == 'w']
    return lst

def white_range():
    '''
    Returns all the squares the white pieces are covering
    '''
    d_zone = []
    lst = find_white()
    for pos in lst:
        sqr = board[pos]
        piece = sqr.piece
        if piece.name[2:] == 'pawn':
            char, num = pos[0], int(pos[1])
            if char == 'a':
                if 'b' + str(num + 1) not in d_zone:
                    d_zone.append('b' + str(num + 1)) 
            elif char == 'h':
                if 'g' + str(num + 1) not in d_zone:
                    d_zone.append('g' + str(num + 1))
            else:
                if pos_dic[piece.x - 100] + str(num + 1) not in d_zone:
                    d_zone.append(pos_dic[piece.x - 100] + str(num + 1))
                if pos_dic[piece.x + 100] + str(num + 1) not in d_zone:
                    d_zone.append(pos_dic[piece.x + 100] + str(num + 1))
        elif piece.name[2:] == 'king':
            for x in king_paths[piece.pos]:
                if x not in d_zone:
                    d_zone.append(x)
        elif piece.name[2:] == 'knight':
            sqrs = knight_paths[piece.pos]
            for el in sqrs:
                if el not in d_zone:
                    d_zone.append(el)
        elif piece.name[2:] == 'rook':
            sqrs = rook_paths[piece.pos]
            bounds = [t for t in sqrs if out(t)]
            paths = [list(group) for k, group in groupby(sqrs, lambda x: x in bounds) if not k]
            for path in paths:
                for pos in path:
                    sqr = board[pos]
                    if sqr.occ is False:
                        d_zone.append(pos)
                    else:
                        if piece.name[0] != sqr.piece.name[0]:
                            if pos not in d_zone:
                                d_zone.append(pos)
                                if 'king' not in sqr.piece.name:
                                    break
                                else:
                                    None
                        else:
                            if pos not in d_zone:
                                d_zone.append(pos)
                            break 

        elif piece.name[2:] == 'bishop':
            sqrs = bishop_paths[piece.pos]
            bounds = [t for t in sqrs if out(t)]
            paths = [list(group) for k, group in groupby(sqrs, lambda x: x in bounds) if not k]
            for path in paths:
                for pos in path:
                    sqr = board[pos]
                    if sqr.occ is False:
                        d_zone.append(pos)
                    else:
                        if piece.name[0] != sqr.piece.name[0]:
                            if pos not in d_zone:
                                d_zone.append(pos)
                                if 'king' not in sqr.piece.name:
                                    break
                                else:
                                    None
                        else:
                            if pos not in d_zone:
                                d_zone.append(pos)
                            break 

        elif piece.name[2:] == 'queen':
            sqrs = queen_paths[piece.pos]
            bounds = [t for t in sqrs if out(t)]
            paths = [list(group) for k, group in groupby(sqrs, lambda x: x in bounds) if not k]
            for path in paths:
                for pos in path:
                    sqr = board[pos]
                    if sqr.occ is False:
                        d_zone.append(pos)
                    else:
                        if piece.name[0] != sqr.piece.name[0]:
                            if pos not in d_zone:
                                d_zone.append(pos)
                                if 'king' not in sqr.piece.name:
                                    break
                                else:
                                    None
                        else:
                            if pos not in d_zone:
                                d_zone.append(pos)
                            break 
    return d_zone

def black_range():
    '''
    Returns all the squares the white pieces are covering
    '''
    d_zone = []
    lst = find_black()
    for pos in lst:
        sqr = board[pos]
        piece = sqr.piece
        if piece.name[2:] == 'pawn':
            char, num = pos[0], int(pos[1])
            if char == 'a':
                if 'b' + str(num - 1) not in d_zone:
                    d_zone.append('b' + str(num - 1)) 
            elif char == 'h':
                if 'g' + str(num - 1) not in d_zone:
                    d_zone.append('g' + str(num - 1))
            else:
                if pos_dic[piece.x - 100] + str(num - 1) not in d_zone:
                    d_zone.append(pos_dic[piece.x - 100] + str(num - 1))
                if pos_dic[piece.x + 100] + str(num - 1) not in d_zone:
                    d_zone.append(pos_dic[piece.x + 100] + str(num - 1))
        elif piece.name[2:] == 'king':
            for x in king_paths[piece.pos]:
                if x not in d_zone:
                    d_zone.append(x)
        elif piece.name[2:] == 'knight':
            sqrs = knight_paths[piece.pos]
            for el in sqrs:
                if el not in d_zone:
                    d_zone.append(el)
        elif piece.name[2:] == 'rook':
            sqrs = rook_paths[piece.pos]
            bounds = [t for t in sqrs if out(t)]
            paths = [list(group) for k, group in groupby(sqrs, lambda x: x in bounds) if not k]
            for path in paths:
                for pos in path:
                    sqr = board[pos]
                    if sqr.occ is False:
                        d_zone.append(pos)
                    else:
                        if piece.name[0] != sqr.piece.name[0]:
                            if pos not in d_zone:
                                d_zone.append(pos)
                                if 'king' not in sqr.piece.name:
                                    break
                                else:
                                    None
                        else:
                            if pos not in d_zone:
                                d_zone.append(pos)
                            break 

        elif piece.name[2:] == 'bishop':
            sqrs = bishop_paths[piece.pos]
            bounds = [t for t in sqrs if out(t)]
            paths = [list(group) for k, group in groupby(sqrs, lambda x: x in bounds) if not k]
            for path in paths:
                for pos in path:
                    sqr = board[pos]
                    if sqr.occ is False:
                        d_zone.append(pos)
                    else:
                        if piece.name[0] != sqr.piece.name[0]:
                            if pos not in d_zone:
                                d_zone.append(pos)
                                if 'king' not in sqr.piece.name:
                                    break
                                else:
                                    None
                        else:
                            if pos not in d_zone:
                                d_zone.append(pos)
                            break 

        elif piece.name[2:] == 'queen':
            sqrs = queen_paths[piece.pos]
            bounds = [t for t in sqrs if out(t)]
            paths = [list(group) for k, group in groupby(sqrs, lambda x: x in bounds) if not k]
            for path in paths:
                for pos in path:
                    sqr = board[pos]
                    if sqr.occ is False:
                        d_zone.append(pos)
                    else:
                        if piece.name[0] != sqr.piece.name[0]:
                            if pos not in d_zone:
                                d_zone.append(pos)
                                if 'king' not in sqr.piece.name:
                                    break
                                else:
                                    None
                        else:
                            if pos not in d_zone:
                                d_zone.append(pos)
                            break          
    return d_zone

def white_moves():
    '''
    Returns all the moves white can make 
    '''
    moves = []
    for pos in find_white():
        piece = board[pos].piece
        for move in piece.av_moves():
            if move not in moves:
                moves.append(move)
    return moves

def black_moves():
    '''
    Returns all the moves black can make 
    '''
    moves = []
    for pos in find_black():
        piece = board[pos].piece
        for move in piece.av_moves():
            if move not in moves:
                moves.append(move)
    return moves

def draw_board():
    '''
    Draws the initial board
    '''
    dx = sqr_size
    dy = sqr_size
    start_x = 100
    start_y = 100
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                colour = light_brown
            else:
                colour = dark_brown
            sqr = Square(start_x + j*dx, start_y + i*dy, colour)
            board[sqr.pos] = sqr
            sqr.draw()
    return

up = False
def start():
    draw_board()
    from_FEN('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w')
    pygame.display.update()

def move(piece: Piece, new_pos: str, curr_pos=None):
    '''
    Moves a piece from its current position to the position given by pos
    '''
    global up, kings_pos 
    if curr_pos is None:
        cp = piece.pos
    else:
        cp = curr_pos
    pos = new_pos
    #Updating the square the piece is moving from
    curr_sqr = board[cp]
    curr_sqr.occ = False
    curr_sqr.piece = None
    curr_sqr.piece_history.append(piece)
    curr_sqr.draw()
    #Updating the square the piece is moving to
    next_sqr = board[pos]
    next_sqr.piece_history.append(next_sqr.piece)
    next_sqr.piece = piece
    next_sqr.occ = True
    next_sqr.draw()
    piece.prev_pos = curr_sqr.pos
    piece.dummy_place(pos)
    if piece.name == 'w_king':   #Updating the positions of the white and black king
        kings_pos['w'] = pos
    elif piece.name == 'b_king':
        kings_pos['b'] = pos
    up = False
    return

def blip():
    '''Updates the display'''
    fen = to_FEN()
    from_FEN(fen)
    pygame.display.update()
    return

def sqr_selection(x: float, y: float):
    '''
    Converts a mouse input to a square we recognize
    '''
    x_1 = x - x % 100
    y_1 = (1000-y) // 100
    if x_1 in pos_dic.keys() and y_1 in [t for t in range(1, 9)]:
        return pos_dic[x_1] + str(y_1)
    else:
        return 'xx'

def indicate(piece: Piece):
    '''
    Drawns an indicator for all the available squares a piece can move to
    '''
    for el in piece.av_moves():
        box = board[el]
        if box.occ is False:
            x, y = box.x, box.y
            pygame.draw.circle(screen, green, (x+50, y+50), 15)
        pygame.display.update()
    return

def select(sqr: Square):
    '''
    Draws a border around the selected square
    '''
    draw_rect(green, sqr)
    return 

def remove_selection(sqr: Square):
    '''
    Removes the indicator od a square
    '''
    draw_rect(sqr.colour, sqr)
    return

def rem_inds(piece: Piece):
    '''
    Remove the indicators of available squares
    '''
    for pos in piece.av_moves():
        box = board[pos]
        if box.occ is False:
            box.draw()
            pygame.display.update()
    return

turn = 1
queue = []
move_log = []
white_turn = True
player_turn = True

def en_passant(pawn):
    '''Checking for the possibility of en passant'''
    global move_log
    can_take = []
    if len(move_log) > 0:
        previous_move = move_log[-1]
        previous_piece, previous_pos = previous_move[0], previous_move[1]
        if pawn.pos[1] == '5':
            if pawn.pos[0] == 'a':
                if previous_piece.name == 'b_pawn' and previous_pos == 'b5' and previous_piece.num_of_moves == 1:
                    can_take.append('b6')
            elif pawn.pos[0] == 'h':
                if previous_piece.name == 'b_pawn' and previous_pos == 'g5' and previous_piece.num_of_moves == 1:
                    can_take.append('g6')
            else:
                ind1 = positions.index(pawn.pos)
                ind2 = positions.index(previous_pos)
                if previous_piece.name == 'b_pawn' and abs(ind1 - ind2) == 8  and previous_piece.num_of_moves == 1:
                    can_take.append(previous_pos[0] + '6')
        elif pawn.pos[1] == '4':
            if pawn.pos[0] == 'a':
                if previous_piece.name == 'w_pawn' and previous_pos == 'b4' and previous_piece.num_of_moves == 1:
                    can_take.append('b3')
            elif pawn.pos[0] == 'h':
                if previous_piece.name == 'w_pawn' and previous_pos == 'g4' and previous_piece.num_of_moves == 1:
                    can_take.append('g3')
            else:
                ind1 = positions.index(pawn.pos)
                ind2 = positions.index(previous_pos)
                if previous_piece.name == 'w_pawn' and abs(ind1 - ind2) == 8  and previous_piece.num_of_moves == 1:
                    can_take.append(previous_pos[0] + '3')
        else:
            None
    else:
        None
    return can_take

def castle_king_side(king: Piece):
    '''
    Checks whether a king can castle king side
    '''
    num = king.num
    king_rook = board['h' + str(num)].piece
    fen = to_FEN()
    turn_player = fen.split(sep=' ')[1]
    if king_rook is None:
        return False
    if white_in_check() or black_in_check():
        return False
    else:
        if not king.num_of_moves == 0 or not king_rook.num_of_moves == 0:
            return False
        else:
            if turn_player == 'w':
                if white_in_check():
                    return False
                else:
                    if 'f1' in black_range() or 'g1' in black_range():
                        return False
                    else:
                        if board['h1'].occ is False or board['f1'].occ is True or board['g1'].occ is True:
                            return False
                        else:
                            return True
            else:
                if black_in_check():
                    return False
                else:
                    if 'f8' in white_range() or 'g8' in white_range():
                        return False
                    else:
                        if board['h8'].occ is False or board['f8'].occ is True or board['g8'].occ is True:
                            return False
                        else:
                            return True

def castle_queen_side(king: Piece):
    '''
    Checks whether a king can castle queen side
    '''
    num = king.num
    queen_rook = board['a' + str(num)].piece
    fen = to_FEN()
    turn_player = fen.split(sep=' ')[1]
    if queen_rook is None:
        return False
    if white_in_check() or black_in_check():
        return False

    else:
        if not king.num_of_moves == 0 or not queen_rook.num_of_moves == 0:
            return False
        else:
            if turn_player == 'w':
                if white_in_check():
                    return False
                else:
                    if 'd1' in black_range() or 'c1' in black_range():
                        return False
                    else:
                        if board['a1'].occ is False or board['d1'].occ is True or board['c1'].occ is True:
                            return False
                        else:
                            if board['b1'].occ is True:
                                return False
                            else:
                                return True
            else:
                if black_in_check():
                    return False
                else:
                    if 'd8' in white_range() or 'c8' in white_range():
                        return False
                    else:
                        if board['a8'].occ is False or board['d8'].occ is True or board['c8'].occ is True:
                            return False
                        else:
                            if board['b8'].occ is True:
                                return False
                            else:
                                return True

def is_mate(fen):
    '''
    Checks for checkmate
    '''
    poss_fens = ply1(fen)
    mate = len(poss_fens) == 0
    return mate

def turn_move(new_sqr: Square, curr_pos: str=None):
    '''
    The most important function which prescribes what the main loop should do.
    It takes a sqr as an input and then checks whether we have a piece lined up in the queue to move or not.
    '''
    global queue, player_turn, up
    sqr = new_sqr

    if player_turn:
        if sqr.occ is False:
            if len(queue) == 0:
                up = True
            else:
                piece = queue.pop()
                if sqr.pos in piece.av_moves():
                    rem_inds(piece)
                    remove_selection(board[piece.pos])
                    if up:
                        if piece.name == 'w_king':
                            if sqr.pos == 'c1':
                                if castle_queen_side(piece):
                                    move(piece, sqr.pos)
                                    move(board['a1'].piece, 'd1')
                                else:
                                    move(piece, sqr.pos)
                            elif sqr.pos == 'g1':
                                if castle_king_side(piece):
                                    move(piece, 'g1')
                                    move(board['h1'].piece, 'f1')
                                else:
                                    move(piece, sqr.pos)
                            else:
                                move(piece, sqr.pos)
                        elif 'pawn' in piece.name:
                            white_ep = sqr.pos[0] + '5'
                            if sqr.pos[1] == '8':
                                move(piece, sqr.pos)
                                prom_queen = Piece(w_queen)
                                prom_queen.dummy_place(sqr.pos)
                                sqr.piece = prom_queen
                            elif sqr.pos[1] == '6' and abs(positions.index(piece.pos) - positions.index(white_ep)) == 8:
                                move(piece, sqr.pos)
                                sqr2_pos = sqr.pos[0] + '5'
                                sqr2 = board[sqr2_pos]
                                sqr2.piece = None
                                sqr2.occ = False
                                sqr2.draw()
                            else:
                                move(piece, sqr.pos)
                        else:
                            move(piece, sqr.pos)
                else:
                    rem_inds(piece)
                    remove_selection(board[piece.pos])
        else:
            curr_piece = sqr.piece
            if curr_piece.name[0] == 'w':
                if len(queue) == 0:
                    indicate(curr_piece)
                    select(sqr)
                    queue.append(curr_piece)
                    up = True
                else:
                    prev_piece = queue.pop()
                    remove_selection(board[prev_piece.pos])
                    rem_inds(prev_piece)
                    indicate(curr_piece)
                    select(sqr)
                    queue.append(curr_piece)
            else:
                if len(queue) > 0:
                    piece = queue.pop()
                    if sqr.pos in piece.av_moves():
                        remove_selection(board[piece.pos])
                        rem_inds(piece)
                        if up:
                            if 'pawn' in piece.name:
                                if sqr.pos[1] == '8':
                                    move(piece, sqr.pos)
                                    prom_queen = Piece(w_queen)
                                    prom_queen.dummy_place(sqr.pos)
                                    sqr.piece = prom_queen
                                else:
                                    move(piece, sqr.pos)
                            else:
                                move(piece, sqr.pos)
                    else:
                        remove_selection(board[piece.pos])
                        rem_inds(piece)
                else:
                    up = True
    else:
        piece = queue.pop()
        if 'pawn' in piece.name:
            black_ep = sqr.pos[0] + '4'
            white_ep = sqr.pos[0] + '5'
            if sqr.pos[1] == '1':
                move(piece, sqr.pos, curr_pos)
                prom_queen = Piece(b_queen)
                prom_queen.dummy_place(sqr.pos)
                sqr.piece = prom_queen
            elif sqr.pos[1] == '8':
                move(piece, sqr.pos, curr_pos)
                prom_queen = Piece(w_queen)
                prom_queen.dummy_place(sqr.pos)
                sqr.piece = prom_queen
            elif sqr.pos[1] == '6' and abs(positions.index(piece.pos) - positions.index(white_ep)) == 8:
                move(piece, sqr.pos, curr_pos)
                sqr2_pos = white_ep
                sqr2 = board[sqr2_pos]
                sqr2.piece = None
                sqr2.occ = False
                sqr2.draw()
            elif sqr.pos[1] == '3' and abs(positions.index(piece.pos) - positions.index(white_ep)) == 8:
                move(piece, sqr.pos, curr_pos)
                sqr2_pos = black_ep
                sqr2 = board[sqr2_pos]
                sqr2.piece = None
                sqr2.occ = False
                sqr2.draw()
            else:
                move(piece, sqr.pos, curr_pos)
        elif piece.name == 'w_king':
            if sqr.pos == 'c1':
                if castle_queen_side(piece):
                    move(piece, sqr.pos, curr_pos)
                    move(board['a1'].piece, 'd1')
                else:
                    move(piece, sqr.pos, curr_pos)
            elif sqr.pos == 'g1':
                if castle_king_side(piece):
                    move(piece, sqr.pos, curr_pos)
                    move(board['h1'].piece, 'f1')
                else:
                    move(piece, sqr.pos, curr_pos)
            else:
                move(piece, sqr.pos, curr_pos)
        elif piece.name == 'b_king':
            if sqr.pos == 'c8':
                if castle_queen_side(piece):
                    move(piece, sqr.pos, curr_pos)
                    move(board['a8'].piece, 'd8')
                else:
                    move(piece, 'c8')
            elif sqr.pos == 'g8':
                if castle_king_side(piece):
                    move(piece, sqr.pos, curr_pos)
                    move(board['h8'].piece, 'f8')
                else:
                    move(piece, sqr.pos, curr_pos)
            else:
                move(piece, sqr.pos, curr_pos)
        else:
            move(piece, sqr.pos, curr_pos)
    return 

def white_in_check():
    '''
    Returns whether or not white is in check
    '''
    find_white_king = kings_pos['w']
    return find_white_king in black_range()

def black_in_check():
    '''
    Returns whether or not black is in check
    '''
    find_black_king = kings_pos['b']
    return find_black_king in white_range()

to_fen_dic = {'w_pawn' : 'P', 'w_bishop' : 'B', 'w_knight' : 'N', 'w_rook' : 'R', 'w_queen' : 'Q', 'w_king' : 'K',
              'b_pawn' : 'p', 'b_bishop' : 'b', 'b_knight' : 'n', 'b_rook' : 'r', 'b_queen' : 'q', 'b_king' : 'k',
             }
from_fen_dic = {'P' : w_pawn, 'B' : w_bishop, 'N' : w_knight, 'R' : w_rook, 'Q' : w_queen, 'K' : w_king,
                'p' : b_pawn, 'b' : b_bishop, 'n' : b_knight, 'r' : b_rook, 'q' : b_queen, 'k' : b_king
               }

def to_FEN():
    global white_turn
    fen = ''
    count = 0
    for pos in positions:
        sqr = board[pos]
        if sqr.occ:
            if count != 0:
                char = str(count)
                count = 0
            else:
                char = ''
            char += to_fen_dic[sqr.piece.name]
            if pos[0] == 'h':
                if pos[1] == '1':
                    None
                else:
                    char += '/'
        else:
            count += 1
            if pos[0] == 'h':
                if pos[1] == '1':
                    char = str(count)
                else:
                    char = str(count) + '/'
                count = 0
            else:
                char = ''
        fen += char
    fen += ' '
    if white_turn:
        fen += 'w'
    else:
        fen += 'b'
    return fen

nom_dic = {pos : 0 for pos in positions}
def from_FEN(fen_str: str):
    draw_board()
    nums = '123456789'
    count = 0
    fen = fen_str.split(sep=' ')[0]
    for char in fen:
        if char in nums:
            for k in range(int(char)):
                sqr = board[positions[count+k]]
                sqr.occ = False
                sqr.piece = None
                sqr.draw()
            count += int(char)
        elif char == '/':
            pass
        else:
            sqr = board[positions[count]]
            piece = Piece(from_fen_dic[char], nom_dic[sqr.pos])
            piece.place(positions[count])
            count += 1
    for pos in find_white():
        piece_name = board[pos].piece.name
        if piece_name == 'w_king':
            kings_pos['w'] = pos
    for pos in find_black():
        piece_name = board[pos].piece.name
        if piece_name == 'b_king':
            kings_pos['b'] = pos
    return
  
def from_FEN_dummy(fen_str: str):
    nums = '123456789'
    count = 0
    fen = fen_str.split(sep=' ')[0]
    for char in fen:
        if char in nums:
            for k in range(int(char)):
                sqr = board[positions[count+k]]
                sqr.occ = False
                sqr.piece = None
            count += int(char)
        elif char == '/':
            pass
        else:
            sqr = board[positions[count]]
            piece = Piece(from_fen_dic[char], nom_dic[sqr.pos])
            piece.dummy_place(sqr.pos)
            sqr.piece = piece
            sqr.occ = True
            count += 1
    for pos in find_white():
        piece_name = board[pos].piece.name
        if piece_name == 'w_king':
            kings_pos['w'] = pos
    for pos in find_black():
        piece_name = board[pos].piece.name
        if piece_name == 'b_king':
            kings_pos['b'] = pos
    return

def add_mat(fen):
    '''
    Adding up the material on the board and asigning score. If white has more material, score will be positive. 
    If black has more material, score will be negative
    '''
    from_FEN_dummy(fen)
    score = 0
    vals = {'pawn' : 1, 'knight' : 3, 'bishop' : 3, 'rook' : 5, 'queen' : 9, 'king' : 100}
    for pos in find_white():
        piece = board[pos].piece
        score += vals[piece.name[2:]]
    for pos in find_black():
        piece = board[pos].piece
        score -= vals[piece.name[2:]]
    return score

def sgn(char):
    if char == 'w':
        return 1
    elif char == 'b':
        return -1
    else:
        None

def eval(fen):
    '''
    Function we will use to evaluate a given position, represented by a fen string.
    Currently, this is done by evaluating the material and other factors
    The more positive the evaluation is, the better white is and vice-versa.
    '''
    global turn

    #Setting up the board
    from_FEN_dummy(fen)
    
    turn_player = fen.split(sep=' ')[1]
    mid_cols, mid_rows = 'cdef', '3456'
    white_pieces, black_pieces = [board[x].piece for x in find_white()], [board[y].piece for y in find_black()]
    white_pawns = [piece for piece in white_pieces if 'pawn' in piece.name]
    black_pawns = [piece for piece in black_pieces if 'pawn' in piece.name]
    white_king, black_king = board[kings_pos['w']].piece, board[kings_pos['b']].piece 
    #sign = sgn(turn_player)
    #mate = 1000 if is_mate(fen) else 0
    #setting the overall score to -1000 if white is mated and 1000 if black is mated, else, for now set to 0
    #overall_score = -sign * mate
    overall_score = 0
    mat_score = add_mat(fen)
    white_activity = (2*len(white_moves()) + 3*len(white_range()))/5
    black_activity = (2*len(black_moves()) + 3*len(black_range()))/5
    white_mid_pres, black_mid_pres = 0, 0
    w_king_safety, b_king_safety = 0, 0
    w_atk_potential, b_atk_potential = 0, 0
    
    #Checking for castling, castling is usually good
    if castle_king_side(white_king):
        w_king_safety += 3
    if castle_king_side(black_king):
        b_king_safety += 3
    if castle_queen_side(white_king):
        w_king_safety += 3
    if castle_queen_side(black_king):
        b_king_safety += 3
    
    #Updating Kings safety, if there is pawns around the king, it is typically safer
    for pos in king_paths[white_king.pos]:
        sqr = board[pos]
        if sqr.occ and sqr.piece.name == 'w_pawn':
            w_king_safety += 1
    for pos in king_paths[black_king.pos]:
        sqr = board[pos]
        if sqr.occ and sqr.piece.name == 'b_pawn':
            b_king_safety += 1

    #Checking the pawn structure
    w_pawn_poss = [pawn.pos[0] for pawn in white_pawns]
    b_pawn_poss = [pawn.pos[0] for pawn in black_pawns]
    unq_wpp, unq_bpp = list(set(w_pawn_poss)), list(set(b_pawn_poss))
    w_pawn_structure = len(unq_wpp) - len(w_pawn_poss)
    b_pawn_structure = len(unq_bpp) - len(b_pawn_poss)
    
    #Checking for mid presences and attacking potential
    for piece in white_pieces:
        if piece.pos[0] in mid_cols and piece.pos[1] in mid_rows:
            white_mid_pres += 1
        for pos in piece.av_moves():
            if pos in king_paths[black_king.pos]:
                w_atk_potential += 1

    for piece in black_pieces:
        if piece.pos[0] in mid_cols and piece.pos[1] in mid_rows:
            black_mid_pres += 1
        for pos in piece.av_moves():
            if pos in king_paths[white_king.pos]:
                b_atk_potential += 1

    # Updating the overall score
    # w1 - king safety, w2 - activity, w3 - material, w4 - mid pres, w5 - atk potential, w6 - pawn structure
    w1, w2, w3, w4, w5, w6 = 0.14, 0.16, 0.50, 0.05, 0.13, 0.02

    overall_score += w1 * (w_king_safety - b_king_safety)
    overall_score += w2 * (white_activity - black_activity)
    overall_score += w3 * mat_score
    overall_score += w4 * (white_mid_pres - black_mid_pres)
    overall_score += w5 * (w_atk_potential - b_atk_potential)
    overall_score += w6 * (w_pawn_structure - b_pawn_structure)

    return overall_score

def ply1(fen):
    global queue, white_turn

    possible_moves_list = []
    from_FEN_dummy(fen)
    if fen.split(sep=' ')[1] == 'w':
        white_turn = True
        white_pieces = [board[pos].piece for pos in find_white()]
        for piece in white_pieces:
            cp = piece.pos
            queue.append(piece)
            for poss_move in piece.av_moves():
                from_FEN_dummy(fen)
                sqr = board[poss_move]
                turn_move(sqr, cp)
                queue.append(piece)
                if white_in_check():
                    from_FEN_dummy(fen)
                else:
                    new_fen = to_FEN().split(sep=' ')[0]
                    possible_moves_list.append(new_fen + ' b')
            from_FEN_dummy(fen)
    else:
        white_turn = False
        black_pieces = [board[pos].piece for pos in find_black()]
        for piece in black_pieces:
            cp = piece.pos
            queue.append(piece)
            for poss_move in piece.av_moves():
                from_FEN_dummy(fen)
                sqr = board[poss_move]
                turn_move(sqr, cp)
                queue.append(piece)
                if black_in_check():
                    from_FEN_dummy(fen)
                else:
                    new_fen = to_FEN().split(sep=' ')[0]
                    possible_moves_list.append(new_fen + ' w')
            from_FEN_dummy(fen)
    return possible_moves_list

move_scores = {}

def analyze(curr_fen: str, depth: int=1):
    if depth == 1:
        for fen1 in ply1(curr_fen):
            for fen2 in ply1(fen1):
                move_scores[f'{fen2}${fen1}${curr_fen}'] = eval(fen2)    #evaluating function which we will update
        return 
    else:
        analyze(curr_fen, depth-1)
        fm = [key.split(sep='$')[0] for key in move_scores if move_scores[key] <= 0]
        for fen in fm:
            analyze(fen, depth-1)
        return

def choose_move(start_fen: str, n=1):
    analyze(start_fen, depth = n)
    choices = {key : value for key, value in move_scores.items() if key.split(sep='$')[2] == start_fen}
    fms = set([key.split(sep='$')[1] for key in choices])
    fm_scores = {fen : [] for fen in fms}
    if n == 1:
        for mv in fms:
            for key, value in choices.items():
                if key.split(sep='$')[1] == mv:
                    fm_scores[mv].append(value)
                else:
                    None
        scores = {key : max(value) for key, value in fm_scores.items()}
        best_move = min(scores, key=scores.get) 
        return best_move
    elif n == 2:
        ply2 = [key.split(sep='$')[0] for key in choices]
        sms = {key : value for key, value in move_scores.items() if key.split(sep='$')[2] in ply2}
        
    else:
        None

def game():
    '''
    Main game loop   
    '''
    global up, turn, move_log, player_turn, white_turn
    start()
    run = True
    while run:
        white_turn = turn % 2 == 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_0:
                    print(add_mat())
                if event.key == pygame.K_SPACE:
                    start_fen = to_FEN()
                    turn_fen = choose_move(start_fen)
                    from_FEN(turn_fen)
                    blip()
                    if white_in_check():
                        draw_rect(red, board[kings_pos['w']])
                    player_turn = True
                    up = True
                    turn += 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_turn:
                    x, y = pygame.mouse.get_pos()
                    pos = sqr_selection(x, y)
                    if pos not in board.keys():
                        None
                    else:
                        sqr = board[pos]
                        curr_fen = to_FEN()
                        turn_move(sqr)
                        if not up:
                            if white_in_check():
                                from_FEN_dummy(curr_fen)
                                up = True
                            else:
                                king_sqr = board[kings_pos['w']]
                                draw_rect(king_sqr.colour, king_sqr)
                                nom_dic[sqr.piece.pos] += 1
                                blip()
                                turn += 1
                                white_turn = turn % 2 == 1
                                player_turn = False
                            if black_in_check():
                                king_sqr = board[kings_pos['b']]
                                draw_rect(red, king_sqr)
                                if is_mate(to_FEN()):
                                    print('CHECKMATE')
                                else:
                                    None
                            else:
                                king_sqr = board[kings_pos['b']]
                                draw_rect(king_sqr.colour, king_sqr)
                                if len(black_moves()) == 0:
                                    print('DRAW by Stalemate')
                                else:
                                    None
                else:
                    None
    pygame.quit()

if __name__ == '__main__':
    game()
sys.exit()