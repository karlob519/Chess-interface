import pygame
import sys
from itertools import groupby
import sfx
import paths
import clock

#Display
WIDTH, HEIGHT = 1400, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('CHESS')
pygame.font.init()
clock_time = pygame.time.Clock()

#Colours
black = (0, 0, 0)
white = (255, 255, 255)
orange = (255, 128, 10)
light_grey = (200, 200, 200)
dark_grey = (100, 100, 100)
light_blue = (129, 212, 250)
dark_blue = (1, 7, 35)
green = (10, 250, 50)
red = (250, 0, 30)

bg_colour = dark_blue
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

#We will use a dummy piece to check if it is mate or not
dummy_piece = [pygame.image.load('PIECES/w_pawn.png'), 'dummy']

#The inital setup of the board
initial_rows = [[b_rook, b_knight, b_bishop, b_queen, b_king, b_bishop, b_knight, b_rook], 
                [b_pawn for _ in range(8)], 0, 0, 0, 0, [w_pawn for _ in range(8)],
                [w_rook, w_knight, w_bishop, w_queen, w_king, w_bishop, w_knight, w_rook]]

pos_dic = {100 : 'a', 200 : 'b', 300 : 'c', 400 : 'd',
           500 : 'e', 600 : 'f', 700 : 'g', 800 : 'h'
           }

positions = [char + str(num) for char in string[1:] for num in range(1, 9)]
kings_pos = {'w' : 'e1', 'b' : 'e8'}
sqrs_dic = {}
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
        self.piece_history = [None]
        self.pos = self.letter + str(self.num)

    def draw(self):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, sqr_size, sqr_size))


class Piece:
    def __init__(self, piece):
        self.piece = piece[0]
        self.name = piece[1]
        self.prev_pos = [None]
        self.num_of_moves = 0
        
    def place(self, pos):
        self.letter = pos[0]
        self.num = int(pos[1])
        self.x = string.index(self.letter) * 100
        self.pos = pos
        self.curr_sqr = sqrs_dic[self.pos]
        x = string.index(self.letter) * 100
        y = 900 - 100 * self.num
        self.show = pygame.transform.scale(self.piece, (sqr_size - 20, sqr_size - 20))
        self.rect = self.piece.get_rect()
        self.rect = self.rect.move((x + 10, y + 10))
        screen.blit(self.show, self.rect)
        sqrs_dic[self.pos].occ = True
        sqrs_dic[self.pos].piece = self
        sqrs_dic[self.pos].piece_history.append(self)
    
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
                        if sqrs_dic[pos1].occ is False:
                            av_sqrs.append(pos1)
                            if sqrs_dic[pos2].occ is False:
                                av_sqrs.append(pos2)
                        if sqrs_dic[pos3].occ is True and sqrs_dic[pos3].piece.name[0] == 'b':
                            av_sqrs.append(pos3)
                    elif self.letter == 'h':
                        pos1, pos2, pos3 = 'h3', 'h4', 'g3'
                        if sqrs_dic[pos1].occ is False:
                            av_sqrs.append(pos1)
                            if sqrs_dic[pos2].occ is False:
                                av_sqrs.append(pos2)
                        if sqrs_dic[pos3].occ is True and sqrs_dic[pos3].piece.name[0] == 'b':
                            av_sqrs.append(pos3)
                    else:
                        pos1, pos2 = self.letter + '3', self.letter + '4'   
                        pos3, pos4 = pos_dic[self.x-100] + '3', pos_dic[self.x + 100] + '3'
                        if sqrs_dic[pos1].occ is False:
                            av_sqrs.append(pos1)
                            if sqrs_dic[pos2].occ is False:
                                av_sqrs.append(pos2)
                        if sqrs_dic[pos3].occ is True and sqrs_dic[pos3].piece.name[0] == 'b':
                            av_sqrs.append(pos3)
                        if sqrs_dic[pos4].occ is True and sqrs_dic[pos4].piece.name[0] == 'b':
                            av_sqrs.append(pos4)    
                else:
                    if self.letter == 'a':
                        pos1, pos2, pos3 = 'a6', 'a5', 'b6'
                        if sqrs_dic[pos1].occ is False:
                            av_sqrs.append(pos1)
                            if sqrs_dic[pos2].occ is False:
                                av_sqrs.append(pos2)
                        if sqrs_dic[pos3].occ is True and sqrs_dic[pos3].piece.name[0] == 'w':
                            av_sqrs.append(pos3)
                    elif self.letter == 'h':
                        pos1, pos2, pos3 = 'h6', 'h5', 'g6'
                        if sqrs_dic[pos1].occ is False:
                            av_sqrs.append(pos1)
                            if sqrs_dic[pos2].occ is False:
                                av_sqrs.append(pos2)
                        if sqrs_dic[pos3].occ is True and sqrs_dic[pos3].piece.name[0] == 'w':
                            av_sqrs.append(pos3)
                    else:
                        pos1, pos2 = self.letter + '6', self.letter + '5'   
                        pos3, pos4 = pos_dic[self.x-100] + '6', pos_dic[self.x + 100] + '6'
                        if sqrs_dic[pos1].occ is False:
                            av_sqrs.append(pos1)
                            if sqrs_dic[pos2].occ is False:
                                av_sqrs.append(pos2)
                        if sqrs_dic[pos3].occ is True and sqrs_dic[pos3].piece.name[0] == 'w':
                            av_sqrs.append(pos3)
                        if sqrs_dic[pos4].occ is True and sqrs_dic[pos4].piece.name[0] == 'w':
                            av_sqrs.append(pos4)
            else:
                if name[0] == 'w':
                    if letter == 'a':
                        take_right_pos = pos_dic[self.x + 100] + str(num + 1)
                        take_right = sqrs_dic[take_right_pos]
                        check_empty = letter + str(num+1)
                        if sqrs_dic[check_empty].occ is False:
                            av_pos1 = letter + str(num + 1) 
                            av_sqrs.append(av_pos1)
                        if take_right.occ is True:
                            if take_right.piece.name[0] == 'b':
                                av_sqrs.append(take_right.pos)
                    elif letter == 'h':
                        take_left_pos = pos_dic[self.x - 100] + str(num + 1)
                        take_left = sqrs_dic[take_left_pos]
                        check_empty = letter + str(num + 1)
                        if sqrs_dic[check_empty].occ is False:
                            av_pos1 = letter + str(num + 1) 
                            av_sqrs.append(av_pos1)
                        if take_left.occ is True:
                            if take_left.piece.name[0] == 'b':
                                av_sqrs.append(take_left.pos)
                    else:
                        take_left_pos = pos_dic[self.x - 100] + str(num + 1)
                        take_right_pos = pos_dic[self.x + 100] + str(num + 1)
                        take_left = sqrs_dic[take_left_pos]
                        take_right = sqrs_dic[take_right_pos]
                        check_empty = letter + str(num+1)
                        if sqrs_dic[check_empty].occ is False:
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
                        take_right = sqrs_dic[take_right_pos]
                        check_empty = letter + str(num - 1)
                        if sqrs_dic[check_empty].occ is False:
                            av_pos1 = letter + str(num - 1) 
                            av_sqrs.append(av_pos1)
                        if take_right.occ is True:
                            if take_right.piece.name[0] == 'w':
                                av_sqrs.append(take_right.pos)
                    elif letter == 'h':
                        take_left_pos = pos_dic[self.x - 100] + str(num - 1)
                        take_left = sqrs_dic[take_left_pos]
                        check_empty = letter + str(num - 1)
                        if sqrs_dic[check_empty].occ is False:
                            av_sqrs.append(check_empty)
                        if take_left.occ is True:
                            if take_left.piece.name[0] == 'w':
                                av_sqrs.append(take_left.pos)
                    else:
                        take_left_pos = pos_dic[self.x - 100] + str(num - 1)
                        take_right_pos = pos_dic[self.x + 100] + str(num - 1)
                        take_left = sqrs_dic[take_left_pos]
                        take_right = sqrs_dic[take_right_pos]
                        check_empty = letter + str(num - 1)
                        if sqrs_dic[check_empty].occ is False:
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
                sqr = sqrs_dic[el]
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
                    sqr = sqrs_dic[pos]
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
                    sqr = sqrs_dic[pos]
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
                    sqr = sqrs_dic[pos]
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
                    if not check and sqrs_dic[sqr].occ is False:
                        av_sqrs.append(sqr)
                    elif not check and sqrs_dic[sqr].piece.name[0] == 'b':
                        av_sqrs.append(sqr)
                    else:
                        None
            else:
                for sqr in sqrs:
                    check = False
                    if sqr in white_range():
                        check = True 
                    if not check and sqrs_dic[sqr].occ is False:
                        av_sqrs.append(sqr)
                    elif not check and sqrs_dic[sqr].piece.name[0] == 'w':
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
    global sqrs_dic
    lst = [key for key, value in sqrs_dic.items() if value.occ is True and value.piece.name[0] == 'b']
    return lst

def find_white():
    '''
    Returns a list containing the positions of all the white pieces currently on the board
    '''
    global sqrs_dic
    lst = [key for key, value in sqrs_dic.items() if value.occ is True and value.piece.name[0] == 'w']
    return lst

def white_range():
    '''
    Returns all the squares the white pieces are covering
    '''
    d_zone = []
    lst = find_white()
    for pos in lst:
        sqr = sqrs_dic[pos]
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
                    sqr = sqrs_dic[pos]
                    if sqr.occ is False:
                        d_zone.append(pos)
                    else:
                        if pos not in d_zone:
                            d_zone.append(pos)
                            if 'king' not in sqr.piece.name:
                                break
                            else:
                                None
                        else:
                            break

        elif piece.name[2:] == 'bishop':
            sqrs = bishop_paths[piece.pos]
            bounds = [t for t in sqrs if out(t)]
            paths = [list(group) for k, group in groupby(sqrs, lambda x: x in bounds) if not k]
            for path in paths:
                for pos in path:
                    sqr = sqrs_dic[pos]
                    if sqr.occ is False:
                        d_zone.append(pos)
                    else:
                        if pos not in d_zone:
                            d_zone.append(pos)
                            if 'king' not in sqr.piece.name:
                                break
                            else:
                                None
                        else:
                            break

        elif piece.name[2:] == 'queen':
            sqrs = queen_paths[piece.pos]
            bounds = [t for t in sqrs if out(t)]
            paths = [list(group) for k, group in groupby(sqrs, lambda x: x in bounds) if not k]
            for path in paths:
                for pos in path:
                    sqr = sqrs_dic[pos]
                    if sqr.occ is False:
                        d_zone.append(pos)
                    else:
                        if pos not in d_zone:
                            d_zone.append(pos)
                            if 'king' not in sqr.piece.name:
                                break
                            else:
                                None
                        else:
                            break
    return d_zone

def black_range():
    '''
    Returns all the squares the white pieces are covering
    '''
    d_zone = []
    lst = find_black()
    for pos in lst:
        sqr = sqrs_dic[pos]
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
                    sqr = sqrs_dic[pos]
                    if sqr.occ is False:
                        d_zone.append(pos)
                    else:
                        if pos not in d_zone:
                            d_zone.append(pos)
                            if 'king' not in sqr.piece.name:
                                break
                        else:
                            break

        elif piece.name[2:] == 'bishop':
            sqrs = bishop_paths[piece.pos]
            bounds = [t for t in sqrs if out(t)]
            paths = [list(group) for k, group in groupby(sqrs, lambda x: x in bounds) if not k]
            for path in paths:
                for pos in path:
                    sqr = sqrs_dic[pos]
                    if sqr.occ is False:
                        d_zone.append(pos)
                    else:
                        if pos not in d_zone:
                            d_zone.append(pos)
                            if 'king' not in sqr.piece.name:
                                break
                        else:
                            break

        elif piece.name[2:] == 'queen':
            sqrs = queen_paths[piece.pos]
            bounds = [t for t in sqrs if out(t)]
            paths = [list(group) for k, group in groupby(sqrs, lambda x: x in bounds) if not k]
            for path in paths:
                for pos in path:
                    sqr = sqrs_dic[pos]
                    if sqr.occ is False:
                        d_zone.append(pos)
                    else:
                        if pos not in d_zone:
                            d_zone.append(pos)
                            if 'king' not in sqr.piece.name:
                                break
                        else:
                            break                
    return d_zone

def white_moves():
    '''
    Returns all the moves white can make 
    '''
    moves = []
    for pos in find_white():
        piece = sqrs_dic[pos].piece
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
        piece = sqrs_dic[pos].piece
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
                colour = white
            else:
                colour = black
            sqr = Square(start_x + j*dx, start_y + i*dy, colour)
            sqrs_dic[sqr.pos] = sqr
            sqr.draw()
    return

def set_pieces():
    '''
    Setting up the board at the start of the game
    '''
    for num in [1, 2, 7, 8]:
        for i in range(1, 9):
            row = initial_rows[8-num]
            char = string[i]
            pos = char + str(num)
            val = row[i-1]
            piece = Piece(val)
            piece.place(pos)
    return

up = False
def start():
    sfx.intro()
    draw_board()
    set_pieces()
    pygame.display.update()

def move(piece: Piece, pos: str):
    '''
    Moves a piece from its current position to the position given by pos
    '''
    global up, kings_pos 
    curr_sqr = piece.curr_sqr
    curr_sqr.occ = False
    curr_sqr.piece = None
    curr_sqr.draw()
    next_sqr = sqrs_dic[pos]
    next_sqr.piece_history.append(next_sqr.piece)
    next_sqr.piece = piece
    next_sqr.occ = True
    piece.prev_pos.append(curr_sqr.pos)
    piece.place(pos)
    if piece.name == 'w_king':   #Updating the positions of the white and black king
        kings_pos['w'] = pos
    elif piece.name == 'b_king':
        kings_pos['b'] = pos
    up = False
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
        box = sqrs_dic[el]
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
        box = sqrs_dic[pos]
        if box.occ is False:
            box.draw()
            pygame.display.update()
    return

turn = 1
queue = []
move_log = []
white_turn = True

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
    king_rook = sqrs_dic['h' + str(num)].piece
    if king_rook is None:
        return False
    if white_in_check() or black_in_check():
        return False
    else:
        if not king.num_of_moves == 0 or not king_rook.num_of_moves == 0:
            return False
        else:
            if white_turn:
                if white_in_check():
                    return False
                else:
                    if 'f1' in black_range() or 'g1' in black_range():
                        return False
                    else:
                        if sqrs_dic['h1'].occ is False or sqrs_dic['f1'].occ is True or sqrs_dic['g1'].occ is True:
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
                        if sqrs_dic['h8'].occ is False or sqrs_dic['f8'].occ is True or sqrs_dic['g8'].occ is True:
                            return False
                        else:
                            return True

def castle_queen_side(king: Piece):
    '''
    Checks whether a king can castle queen side
    '''
    num = king.num
    queen_rook = sqrs_dic['a' + str(num)].piece
    if queen_rook is None:
        return False
    if white_in_check() or black_in_check():
        return False

    else:
        if not king.num_of_moves == 0 or not queen_rook.num_of_moves == 0:
            return False
        else:
            if white_turn:
                if white_in_check():
                    return False
                else:
                    if 'd1' in black_range() or 'c1' in black_range():
                        return False
                    else:
                        if sqrs_dic['a1'].occ is False or sqrs_dic['d1'].occ is True or sqrs_dic['c1'].occ is True:
                            return False
                        else:
                            if sqrs_dic['b1'].occ is True:
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
                        if sqrs_dic['a8'].occ is False or sqrs_dic['d8'].occ is True or sqrs_dic['c8'].occ is True:
                            return False
                        else:
                            if sqrs_dic['b8'].occ is True:
                                return False
                            else:
                                return True

def is_mate():
    '''
    Checks for checkmate
    '''
    blocker_sqr = Square(100, 0, bg_colour)
    blocker_pos = blocker_sqr.pos
    sqrs_dic[blocker_pos] = blocker_sqr
    blocker = Piece(dummy_piece)
    blocker.curr_sqr = sqrs_dic[blocker_pos]
    mate = True
    if white_turn: 
        king_pos = kings_pos['b']
        atks = []
        for pos in find_white():
            if king_pos in sqrs_dic[pos].piece.av_moves():
                atks.append(sqrs_dic[pos].piece)
        king = sqrs_dic[king_pos].piece
        esc_sqrs = king.av_moves()
        if not esc_sqrs:
            if len(atks) == 1:
                piece = atks[0]
                if piece.pos in black_moves():
                    mate = False
                else:
                    for pos in piece.av_moves(): 
                        if pos in black_moves() and pos != king_pos:
                            move(blocker, pos)
                            if not black_in_check():
                                mate = False
                                move(blocker, blocker_pos)
                                blocker_sqr.draw()
                                break
                            else:
                                move(blocker, blocker_pos)
                                blocker_sqr.draw()
            else:
                None
        else:
            piece = atks[0]
            if piece.pos in black_moves():
                mate = False
            else:
                for pos in esc_sqrs:
                    move(king, pos)
                    piece = sqrs_dic[pos].piece_history[-1]
                    if not black_in_check():
                        mate = False
                        move(king, king.prev_pos[-1])
                        if piece is not None:
                            move(piece, piece.pos)
                        break
                    else:
                        move(king, king.prev_pos[-1])
                        if piece is not None:
                            move(piece, piece.pos)
                draw_rect(red, sqrs_dic[king_pos])
    else:
        king_pos = kings_pos['w']
        atks = []
        for pos in find_black():
            if king_pos in sqrs_dic[pos].piece.av_moves():
                atks.append(sqrs_dic[pos].piece)
        king = sqrs_dic[king_pos].piece
        esc_sqrs = king.av_moves()
        if not esc_sqrs:
            if len(atks) == 1:
                piece = atks[0]
                if piece.pos in white_moves():
                    mate = False
                else:
                    for pos in piece.av_moves(): 
                        if pos in white_moves() and pos != king_pos:
                            move(blocker, pos)
                            if not white_in_check():
                                mate = False
                                move(blocker, blocker_pos)
                                blocker_sqr.draw()
                                break
                            else:
                                move(blocker, blocker_pos)
                                blocker_sqr.draw()
            else:
                None
        else:
            piece = atks[0]
            if piece.pos in white_moves():
                mate = False
            else:
                for pos in esc_sqrs:
                    move(king, pos)
                    piece = sqrs_dic[pos].piece_history[-1]
                    if not white_in_check():
                        mate = False
                        move(king, king.prev_pos[-1])
                        if piece is not None:
                            move(piece, piece.pos)
                        break
                    else:
                        move(king, king.prev_pos[-1])
                        if piece is not None:
                            move(piece, piece.pos)
                draw_rect(red, sqrs_dic[king_pos])
    return mate

courser = -1
def back():
    '''
    Goes back one move
    '''
    global move_log, turn, courser
    if len(move_log) > 0:
        previous_move = move_log.pop()
        piece, curr_pos = previous_move[0], previous_move[1]
        prev_pos = piece.prev_pos[courser]
        piece.num_of_moves -= 1
        move(piece, prev_pos)
        if sqrs_dic[curr_pos].piece_history[courser-1] is not None:
            prev_piece = sqrs_dic[curr_pos].piece_history.pop(courser-1)
            prev_piece.place(curr_pos)
        else:
            None
        turn -= 1
        courser -= 1
        pygame.display.update()
    else:
        None

def turn_move(sqr: Square):
    '''
    The most important function which prescribes what the main loop should do.
    It takes a sqr as an input and then checks whether we have a piece lined up in the queue to move or not.
    '''
    global queue, white_turn, turn, up
    sound = None
    if sqr.occ is False:
        if len(queue) == 0:
            up = True
        else:
            piece = queue.pop()
            if sqr.pos in piece.av_moves():
                rem_inds(piece)
                piece.prev_pos.append(piece.pos)
                remove_selection(sqrs_dic[piece.prev_pos[-1]])
                if up:
                    if piece.name == 'w_king':
                        if sqr.pos == 'c1':
                            if castle_queen_side(piece):
                                move(piece, sqr.pos)
                                move(sqrs_dic['a1'].piece, 'd1')
                                sound = sfx.castling
                            else:
                                move(piece, sqr.pos)
                                sound = sfx.move
                        elif sqr.pos == 'g1':
                            if castle_king_side(piece):
                                move(piece, 'g1')
                                move(sqrs_dic['h1'].piece, 'f1')
                                sound = sfx.castling
                            else:
                                move(piece, sqr.pos)
                                sound = sfx.move
                        else:
                            move(piece, sqr.pos)
                            sound = sfx.move
                    elif piece.name == 'b_king':
                        if sqr.pos == 'c8':
                            if castle_queen_side(piece):
                                move(piece, 'c8')
                                move(sqrs_dic['a8'].piece, 'd8')
                                sound = sfx.castling
                            else:
                                move(piece, 'c8')
                                sound = sfx.move
                        elif sqr.pos == 'g8':
                            if castle_king_side(piece):
                                move(piece, 'g8')
                                move(sqrs_dic['h8'].piece, 'f8')
                                sound = sfx.castling
                            else:
                                move(piece, 'g8')
                                sound = sfx.move
                        else:
                            move(piece, sqr.pos)
                            sound = sfx.move
                    elif 'pawn' in piece.name:
                        white_ep = sqr.pos[0] + '5'
                        black_ep = sqr.pos[0] + '4'
                        if sqr.pos[1] == '8':
                            move(piece, sqr.pos)
                            sound = sfx.promotion
                            prom_queen = Piece(w_queen)
                            sqr.draw()
                            prom_queen.place(sqr.pos)
                            sqr.piece = prom_queen
                        elif sqr.pos[1] == '1':
                            move(piece, sqr.pos)
                            sound = sfx.promotion
                            prom_queen = Piece(b_queen)
                            sqr.draw()
                            prom_queen.place(sqr.pos)
                            sqr.piece = prom_queen
                        elif sqr.pos[1] == '6' and abs(positions.index(piece.pos) - positions.index(white_ep)) == 8:
                            move(piece, sqr.pos)
                            sound = sfx.capture
                            sqr2_pos = sqr.pos[0] + '5'
                            sqr2 = sqrs_dic[sqr2_pos]
                            sqr2.draw()
                            sqr2.piece = None
                            sqr2.occ = False
                        elif sqr.pos[1] == '3' and abs(positions.index(piece.pos) - positions.index(black_ep)) == 8:
                            move(piece, sqr.pos)
                            sound = sfx.capture
                            sqr2_pos = sqr.pos[0] + '4'
                            sqr2 = sqrs_dic[sqr2_pos]
                            sqr2.draw()
                            sqr2.piece = None
                            sqr2.occ = False
                        else:
                            move(piece, sqr.pos)
                            sound = sfx.move
                    else:
                        move(piece, sqr.pos)
                        sound = sfx.move
            else:
                rem_inds(piece)
                remove_selection(sqrs_dic[piece.pos])                  
    else:
        sound = sfx.capture
        if white_turn:
            curr_piece = sqr.piece
            if curr_piece.name[0] == 'w':
                if len(queue) == 0:
                    indicate(curr_piece)
                    select(sqr)
                    queue.append(curr_piece)
                    up = True
                else:
                    prev_piece = queue.pop()
                    remove_selection(sqrs_dic[prev_piece.pos])
                    rem_inds(prev_piece)
                    indicate(curr_piece)
                    select(sqr)
                    queue.append(curr_piece)
            else:
                if len(queue) > 0:
                    piece = queue.pop()
                    if sqr.pos in piece.av_moves():
                        sqr.draw()
                        remove_selection(sqrs_dic[piece.pos])
                        rem_inds(piece)
                        piece.prev_pos[-1] = piece.pos
                        if up:
                            if 'pawn' in piece.name:
                                if sqr.pos[1] == '8':
                                    move(piece, sqr.pos)
                                    sound = sfx.promotion
                                    prom_queen = Piece(w_queen)
                                    sqr.draw()
                                    prom_queen.place(sqr.pos)
                                    sqr.piece = prom_queen
                                else:
                                    move(piece, sqr.pos)
                            else:
                                move(piece, sqr.pos)
                    else:
                        pygame.display.update()
                        remove_selection(sqrs_dic[piece.pos])
                        rem_inds(piece)
                else:
                    up = True
        else:
            curr_piece = sqr.piece
            if curr_piece.name[0] == 'b':
                if len(queue) == 0:
                    indicate(curr_piece)
                    select(sqr)
                    queue.append(curr_piece)
                    up = True
                else:
                    prev_piece = queue.pop()
                    remove_selection(sqrs_dic[prev_piece.pos])
                    rem_inds(prev_piece)
                    indicate(curr_piece)
                    select(sqr)
                    queue.append(curr_piece)
            else:
                if len(queue) > 0:
                    piece = queue.pop()
                    if sqr.pos in piece.av_moves():
                        sqr.draw()
                        remove_selection(sqrs_dic[piece.pos])
                        rem_inds(piece)
                        piece.prev_pos[-1] = piece.pos
                        sqr.prev_piece = curr_piece
                        if up:
                            if 'pawn' in piece.name:
                                if sqr.pos[1] == '1':
                                    move(piece, sqr.pos)
                                    sound = sfx.promotion
                                    prom_queen = Piece(b_queen)
                                    sqr.draw()
                                    prom_queen.place(sqr.pos)
                                    sqr.piece = prom_queen
                                else:
                                    move(piece, sqr.pos)
                            else:
                                move(piece, sqr.pos)
                    else:   
                        remove_selection(sqrs_dic[piece.pos])
                        rem_inds(piece)
                else:
                    up = True
    return sound

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

def game():
    '''
    Main game loop   
    '''
    global up, turn, courser, move_log, white_turn
    clock1, clock2 = clock.generate_clocks()
    go = False
    start()
    run = True
    while run:
        clock_time.tick(60)
        white_turn = turn % 2 == 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_TAB:
                    sfx.mute()
                if event.key == pygame.K_LEFT:
                    back()
                    clock.change(clock1, clock2)
                if event.key == pygame.K_0:
                    print(black_range())
                if event.key == pygame.K_SPACE:
                    go = clock.start_time()
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            x, y = pygame.mouse.get_pos()
            pos = sqr_selection(x, y)
            if pos not in sqrs_dic.keys():
                None
            else:
                sqr = sqrs_dic[pos]
                sound = turn_move(sqr)
                if not up:
                    if white_turn:
                        if white_in_check():
                            move(sqr.piece, sqr.piece.prev_pos[-2])
                            sqr.piece = sqr.piece_history[-2]
                            if sqr.piece_history[-2] is not None:
                                sqr.piece_history[-2].place(sqr.pos)
                                pygame.display.update()
                            up = True
                            sound = sfx.none
                        else:
                            king_sqr = sqrs_dic[kings_pos['w']]
                            draw_rect(king_sqr.colour, king_sqr)
                            sqr.piece.num_of_moves += 1
                            turn += 1
                            clock.change(clock1, clock2)
                            courser = -1                                
                            move_data = (sqr.piece, sqr.pos)
                            move_log.append(move_data)
                        if black_in_check():
                            sound = sfx.check
                            king_sqr = sqrs_dic[kings_pos['b']]
                            draw_rect(red, king_sqr)
                            if is_mate():
                                sound = sfx.checkmate
                                go = clock.start_time()
                                print('CHECKMATE')
                            else:
                                None
                        else:
                            if len(black_moves()) == 0:
                                print('DRAW by Stalemate')
                                go = clock.start_time()
                            else:
                                None
                    else:
                        if black_in_check():
                            move(sqr.piece, sqr.piece.prev_pos[-2])
                            sqr.piece = sqr.piece_history[-2]
                            if sqr.piece_history[-2] is not None:
                                sqr.piece_history[-2].place(sqr.pos)
                                pygame.display.update()
                            up = True
                            sound = sfx.none
                        else:
                            king_sqr = sqrs_dic[kings_pos['b']]
                            draw_rect(king_sqr.colour, king_sqr)
                            sqr.piece.num_of_moves += 1
                            turn += 1
                            courser = -1
                            clock.change(clock1, clock2)
                            move_data = (sqr.piece, sqr.pos)
                            move_log.append(move_data)
                        if white_in_check():
                            sound = sfx.check
                            king_sqr = sqrs_dic[kings_pos['w']]
                            draw_rect(red, king_sqr)
                            if is_mate():
                                sound = sfx.checkmate
                                go = clock.start_time()
                                print('CHECKMATE')
                            else:
                                None
                        else:
                            if len(white_moves()) == 0:
                                print('DRAW by Stalemate')
                                go = clock.start_time()
                            else:
                                None
                    sound()
                else:
                    None
        if go:
            clock.pass_time(clock1, clock2)
        clock1.draw()
        clock2.draw()
        if clock1.time == 0:
            go = clock.start_time()
            print('White lost on time')
            run = False
        elif clock2.time == 0:
            go = clock.start_time()
            print('Black lost on time')
            run = False
    pygame.quit()

if __name__ == '__main__':
    game()
sys.exit()