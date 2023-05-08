import pygame
import sys

#Display
WIDTH, HEIGHT = 1400, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
#pygame.display.set_caption('Clock')
pygame.font.init()

#Colours
black = (0, 0, 0)
white = (255, 255, 255)
orange = (255, 128, 10)
light_grey = (200, 200, 200)
dark_grey = (70, 70, 70)

bg_colour = dark_grey

clock_font = pygame.font.SysFont(None, 100)

clock_time = pygame.time.Clock()
screen.fill(bg_colour)

middle = 25

def clock_time(time: int): 
    '''
    Return a clock-like time display as a string. Time is measured in seconds.

    Input: 100
    Output: 1:40 

    Input: 250
    Output: 4:10
    '''
    seconds = int(time % 60)
    minutes = int(time // 60)
    if seconds >= 10:
        return f'{minutes}:{seconds}'
    else:
        return f'{minutes}:0{seconds}'

class Clock:
    '''
    Class clock, with the position and size of the clock and the time it will run, starting 
    from time till reaches 0.
    '''
    def __init__(self, x: int, y: int, width: float, height: float,
                 fill_colour: tuple, time_colour: tuple, time: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fill_colour = fill_colour
        self.time_colour = time_colour
        self.time = time
    
    def draw(self):
        write = clock_font.render(clock_time(self.time), 1, self.time_colour)
        pygame.draw.rect(screen, self.fill_colour, (self.x, self.y, self.width, self.height))
        screen.blit(write, (self.x + 1.2*middle, self.y + 0.8*middle))
        pygame.display.update()
    
    def rundown(self):
        '''
        We count down from secs till 0, displaying it in the clock_time format
        '''
        while self.time >= 0:
            clock_time.tick(1)
            self.draw()
            self.time -= 1

# Two clocks, with increment      
# # Player one starts
# We increment by 2 secs
player1 = True
inc = 2

turn_colour = white
hold_colour = black

clock_turn_colour = orange
clock_hold_colour = light_grey

mins = 3
round_time = 60 * mins
t1, t2 = round_time, round_time

clock1_x, clock1_y = 1100, 800
clock_width, clock_height = 200, 100

clock2_x, clock2_y = 1100, 100

def reset():
    global t1, t2, go, player1 
    t1, t2 = round_time, round_time
    player1 = True
    go = False
    return

def generate_clocks():
    global t1, t2, clock1_x, clock1_y, clock2_x, clock2_y, clock_width, clock_height
    global hold_colour, clock_hold_colour
    clock1 = Clock(clock1_x, clock1_y, clock_width, clock_height, clock_hold_colour, hold_colour, t1)
    clock2 = Clock(clock2_x, clock2_y, clock_width, clock_height, clock_hold_colour, hold_colour, t2)

    clock1.draw()
    clock2.draw()
    pygame.display.update()
    return clock1, clock2

go = False
def start_time():
    global go
    go = not go
    return go

def pass_time(clock1, clock2):
    global t1, t2
    if player1 is True:
        clock1.fill_colour = orange
        clock1.time_colour = white
        clock1.time = t1
        if t1 > 0:
            t1 -= 1/60
        else:
            t1 = 0
    else:
        clock2.fill_colour = orange
        clock2.time_colour = white
        clock2.time = t2
        if t2 > 0:
            t2 -= 1/60
        else:
            t2 = 0


def change(clock1, clock2):
    global player1, t1, t2, inc
    if player1 is True:
        t1 += inc
        clock1.time = t1
        clock1.fill_colour = light_grey
        clock1.time_colour = black
    else:
        t2 += inc
        clock2.time = t2
        clock2.fill_colour = light_grey
        clock2.time_colour = black
    clock1.draw()
    clock2.draw()
    player1 = not player1
    return

def swap():
    global player1
    player1 = not player1
    return 
    
def three_2():
    global t1, t2, go, player1
    clock1, clock2 = generate_clocks()

    run = True
    while run:
        clock_time.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_SPACE:
                    start_time()
                elif event.key == pygame.K_RETURN:
                    change(clock1, clock2)
        if go:
            pass_time(clock1, clock2)
        clock1.draw()
        clock2.draw()
    pygame.quit()
    return

#three_2()
#sys.exit()