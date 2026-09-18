#!/usr/bin/python3
import math, os, sys, random, pickle
import numpy as np
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

print(" = = = = = = = = = = = = = = = = = = = = = = = = = ")
print(" =  Breakout-Pi for RetroPie by MS-potilas 2026  = ")
print(" = = = = =  Made with Python and Pygame  = = = = = ")
print(" =  https://github.com/MS-potilas/breakout-pi/   = ")
print(" = = = = = = = = = = = = = = = = = = = = = = = = = ")

STARTTEXT = "BREAKOUT-PI"
STARTTEXT_DELAY = 3000

# change working dir to same as the script's
abspath_ = os.path.abspath(__file__)
dname_ = os.path.dirname(abspath_)
os.chdir(dname_)


# get command line to one variable
try:
    cmdline = " " + (" ".join(sys.argv)) + " "
except:
    cmdline = ""

try:
    with open('.cmdline', "r") as f:
        cmdline = f.readline().strip()
    cmdline = " " + cmdline + " "
except:
    pass

cmdline = cmdline.replace('‑', '-')         # non-breaking hyphen to hyphen (used in README.md)


# Initialize Pygame audio mixer (standard CD quality, 16-bit signed)
pygame.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=512)
# initialize pygame
pygame.init()

# get full screen size (for example 1920x1080 or 1280x720)
display_info = pygame.display.Info()
FULL_SCREEN_W = display_info.current_w
FULL_SCREEN_H = display_info.current_h

FPS = 60

GAME_WIDTH = 690
GAME_HEIGHT = 1060

# overlay image size
OVERLAY_W = 1920
OVERLAY_H = 1080

TOP_OFFSET = 94

WINDOW_W = 690
WINDOW_H = 1080

BALL_WIDTH = 12
BALL_HEIGHT = 9

PADDLE_WIDTH = 46       # <= 42+6   basically like brick (smaller gap)
PADDLE_HEIGHT = 18      # <= 13 + 5

PADDLE_SPEED = 10

PADDLE_Y_FROM_BOTTOM = 106

BRICKS_TOP = 184
BRICK_WIDTH = 43
BRICK_HEIGHT = 14
X_GAP = 5
Y_GAP = 4

WALL_WIDTH = 14


WHITE = (255, 255, 255)
GREY = (225, 231, 225)
DARKGREY = (200, 204, 200)
BLACK = (0, 0, 0)
BLUE = (0, 130, 198)


# don't know if this works on windows or mac
def is_windowing_system():
    if sys.platform == 'windows' or sys.platform == 'darwin': # windows or mac
        return True
    if os.environ.get('DISPLAY'):
        return True
    return False


fullscreen = False
dooverlay = False
doservelight = True
fontgap = False
happyend = True         # new, better ending without player having to lose all balls (default), alter with --nohappyend
aiplay = False
fullfps = False
nocolorstrips = False
mini = False
micro = False
nopause = False
wallshift = 2           # move the wall 2 pixels right, so that it is better centered than in the original
dotextoverlay = True    # display "PLAYER UP" and  "BALL IN PLAY" texts as overlay
greyscale = False
easyblink = False
noscaleswitch = False
authentic = False

if '-easyblink ' in cmdline:
    easyblink = True

if '-bigpaddle ' in cmdline:
    PADDLE_WIDTH *= 2

if '-mini ' in cmdline:
    mini = True

if '-micro ' in cmdline:
    micro = True

if '-noscaleswitch ' in cmdline:
    noscaleswitch = True


if '-notextoverlay ' in cmdline:
    dotextoverlay = False

if '-aiplay ' in cmdline:
    aiplay = True

if '-fullfps ' in cmdline:
    fullfps = True

if '-nocolorstrips ' in cmdline or '-nocolors ' in cmdline or '-monochrome ' in cmdline or '-mono ' in cmdline:
    nocolorstrips = True

if '-nopause ' in cmdline:
    nopause = True

if '-nowallshift ' in cmdline:
    wallshift = 0

if nocolorstrips:
    GREY = WHITE

if '-nohappyend ' in cmdline:
    happyend = False

if "-noservelight " in cmdline:
    doservelight = False


if "-fontgap " in cmdline:
    fontgap = True


if '-authentic ' in cmdline:
    doservelight = False
    happyend = False
    nopause = True
    wallshift = 0
    authentic = True
    soundscaleindex = 7


if (is_windowing_system() and not "-fullscreen " in cmdline) or "-windowed " in cmdline:
    # create a window (under X or Wayland, for example)
    if not mini and not micro:
        TOP_OFFSET = 34 #35
        WINDOW_H = 1060 - 70
    else:
        TOP_OFFSET -= 10
        PADDLE_Y_FROM_BOTTOM -= 10
        WINDOW_H = (GAME_HEIGHT-20) // 2
        WINDOW_W = GAME_WIDTH // 2
        if micro:
            WINDOW_H = (GAME_HEIGHT-20) // 2.5
            WINDOW_W = GAME_WIDTH // 2.5
    dascreen = pygame.display.set_mode((WINDOW_W, WINDOW_H), pygame.RESIZABLE)
else:
    # create full screen display 
    dascreen = pygame.display.set_mode((FULL_SCREEN_W, FULL_SCREEN_H), pygame.FULLSCREEN | pygame.NOFRAME )
    fullscreen = True
    dooverlay = True
    
if "-nobezel " in cmdline:
    dooverlay = False

if mini or micro:
    dooverlay = False


overlayname = ""    
overlay = None
if dooverlay:
    overlayname = "breakout"
    if "-altbezel " in cmdline:
        overlayname = "breakouta"
    try:
        overlay = pygame.image.load(f"images/{overlayname}.png").convert_alpha()
    except:
        overlayname = ""
        dooverlay = False
        pass

if overlayname == 'breakouta':
    GAME_HEIGHT -= 120
    TOP_OFFSET -= 60                 +28
    PADDLE_Y_FROM_BOTTOM -= 60       -28
    dotextoverlay = False


textoverlay = None
if dotextoverlay:
    try:
        textoverlay = pygame.image.load(f"images/textoverlay.png").convert_alpha()
    except:
        dooverlay = False


screen = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))


pygame.display.set_caption("Breakout")
clock = pygame.time.Clock()


RED = (198, 8, 0)
ORANGE = (198, 130, 0)
GREEN = (0, 198, 0)
YELLOW = (198, 204, 0)

# better colors
if '-altcolors ' in cmdline or '-rainbowcolors ' in cmdline:
    GREEN = (198, 204, 0)
    YELLOW = (0, 198, 0)
    
if '-greyscale ' in cmdline or '-grayscale ' in cmdline:
    greyscale = True
    BLUE = (128, 128, 128)
    RED = (63, 63, 63)
    ORANGE = (96, 96, 96)
    GREEN = (144, 144, 144)
    YELLOW = (192, 192, 192)
    textoverlay = pygame.image.load(f"images/textoverlaybw.png")


# game states:
# "ATTRACT"
# "PLAYING"
game_state = "ATTRACT" 

# global 2 player game variables
is_two_player = False
current_player = 1

waiting_for_serve = True
serve_delay_timer = 0       # time when serve delay ends

soundscale_visible = 0

def initial_ball_speed():   # "initial horizontal speed is random" -service manual
    return [random.choice([-5,-4, -3, -2, 2, 3, 4,-5]), 4]

# serve delay "no loger than 4 seconds" (cut it down to 3) -service manual
def get_serve_delay():
    return random.randint(1500, 3000)

# each player's game state
player_data = {
    1: {
        "score": 0,
        "lives": 3,
        "current_wall": 1,
        "hit_counter": 0,
        "highest_row_hit": False,
        "paddle_shrunk": False,
        "bricks_state": []      # bricks left on screen
    },
    2: {
        "score": 0,
        "lives": 3,
        "current_wall": 1,
        "hit_counter": 0,
        "highest_row_hit": False,
        "paddle_shrunk": False,
        "bricks_state": []
    }
}

#resets all player data and starts a new game, either 1-player or two-player
def start_new_game(two_player_mode):
    global game_state, current_player, is_two_player, player_data, soundscale_visible

    #soundscale_visible = pygame.time.get_ticks() + 1500
    
    is_two_player = two_player_mode
    current_player = 1  # Player 1 always starts the game
    game_state = "PLAYING"
    
    # reset player's data
    for p in range(1, 3): # 3!
        player_data[p]["score"] = 0
        player_data[p]["lives"] = 3
        player_data[p]["current_wall"] = 1
        player_data[p]["hit_counter"] = 0
        player_data[p]["highest_row_hit"] = False
        player_data[p]["paddle_shrunk"] = False
        player_data[p]["bricks_state"] = []         # empty list -> create full wall
        
    # restore original paddle size (in case it was shrunk)
    paddle.grow()
    
    # create first brick wall for player 1
    rebuild_brick_wall()
    
    # reet ball and start serve delay
    reset_ball_with_serve_wait()


def save_game_data():
    global player_data, current_player, is_two_player
    try:
        save_current_player_bricks(current_player)
        player_data[1]["hit_counter"] = 0
        player_data[1]["highest_row_hit"] = False
        player_data[1]["paddle_shrunk"] = False
        player_data[2]["hit_counter"] = 0
        player_data[2]["highest_row_hit"] = False
        player_data[2]["paddle_shrunk"] = False
        tallennettava_data = {
            "player_data": player_data,
            "current_player": current_player,
            "is_two_player": is_two_player
        }
        # save to pickle
        with open(".breakout_dump.pkl", "wb") as tiedosto:
            pickle.dump(tallennettava_data, tiedosto)
    except:
        pass

def load_game_data():
    global player_data, current_player, is_two_player
    try:
        with open(".breakout_dump.pkl", "rb") as tiedosto:
            ladattu_data = pickle.load(tiedosto)

        # get variables back
        player_data = ladattu_data["player_data"]
        current_player = ladattu_data["current_player"]
        is_two_player = ladattu_data["is_two_player"]
        if not is_two_player:
            current_player = 1
        # if bricks are empty, don't call load_next_player_bricks, because it creates new bricks if wall is empty
        if player_data[current_player]["bricks_state"] != []:
            load_next_player_bricks(current_player)
    except:
        pass
        

def ball_initial_position():
    return (GAME_WIDTH // 2 + random.randint(-5,5), (GAME_HEIGHT - TOP_OFFSET - BRICKS_TOP - PADDLE_Y_FROM_BOTTOM) // 2 + TOP_OFFSET + BRICKS_TOP)

def reset_to_attract():
    global game_state, waiting_for_serve

    game_state = "ATTRACT"
    waiting_for_serve = False  # no serve wait when switch to attract

    # reset ball position
    ball.rect.center = ball_initial_position()
    # reset ball speed
    ball.velocity = initial_ball_speed()
    load_game_data()
    

def reset_ball_core():
    global serve_delay_timer, paddle
    
    ball.rect.center = ball_initial_position()
    ball.velocity = [0, 0]  # ball does not move first
    
    # Nollataan osumalaskurit
    player_data[current_player]["hit_counter"] = 0
    player_data[current_player]["highest_row_hit"] = False
    paddle.grow()
    player_data[current_player]["paddle_shrunk"] = False
    
    
    serve_delay_timer = 0

# reset ball and start waiing for serve button
def reset_ball_with_serve_wait():
    global waiting_for_serve
    
    reset_ball_core()
    waiting_for_serve = True

    

GLYPHS = {
    '0': ["111", "101", "101", "101", "101", "101", "111"],
    '1': ["001", "001", "001", "001", "001", "001", "001"],
    '2': ["111", "001", "001", "111", "100", "100", "111"],
    '3': ["111", "001", "001", "111", "001", "001", "111"],
    '4': ["101", "101", "101", "111", "001", "001", "001"],
    '5': ["111", "100", "100", "111", "001", "001", "111"],
    '6': ["111", "100", "100", "111", "101", "101", "111"],
    '7': ["111", "001", "001", "001", "001", "001", "001"],
    '8': ["111", "101", "101", "111", "101", "101", "111"],
    '9': ["111", "101", "101", "111", "001", "001", "111"],
    'A': ["010", "101", "101", "111", "101", "101", "101"],
    'B': ["110", "101", "101", "110", "101", "101", "110"],
    'C': ["111", "100", "100", "100", "100", "100", "111"],
    'D': ["110", "101", "101", "101", "101", "101", "110"],
    'E': ["111", "100", "100", "111", "100", "100", "111"],
    'F': ["111", "100", "100", "111", "100", "100", "100"],
    'I': ["010", "010", "010", "010", "010", "010", "010"],
    'J': ["001", "001", "001", "001", "001", "001", "111"],
    'K': ["101", "101", "110", "100", "110", "101", "101"],
    'L': ["100", "100", "100", "100", "100", "100", "111"],
    'M': ["101", "111", "111", "111", "101", "101", "101"],
    'N': ["101", "101", "111", "111", "111", "101", "101"],
    'O': ["111", "101", "101", "101", "101", "101", "111"],
    'P': ["110", "101", "101", "110", "100", "100", "100"],
    'R': ["110", "101", "101", "110", "101", "101", "101"],
    'S': ["111", "100", "100", "111", "001", "001", "111"],
    'T': ["111", "010", "010", "010", "010", "010", "010"],
    'U': ["101", "101", "101", "101", "101", "101", "111"],
    'V': ["101", "101", "101", "101", "101", "111", "010"],
    ':': ["000", "000", "010", "000", "000", "010", "000"],
    ' ': ["000", "000", "000", "000", "000", "000", "000"],
    '-': ["000", "000", "000", "111", "000", "000", "000"],
    '+': ["000", "010", "010", "111", "010", "010", "000"],
}


#  Draws a blocky 1976 arcade-accurate numbers and some characters.
#  block_size = width/height of a single pixel segment within the digit.
def draw_retro_glyphs(surface, score_str, start_x, start_y, block_size=4, color=GREY, centerx=False):
    current_x = start_x
    block_size_y = round(block_size * 0.74)
    if centerx:
        current_x -= (4 * block_size * len(score_str)) // 2
    
    # Process each digit in the score string left-to-right
    for char in score_str:
        if char in GLYPHS:
            matrix = GLYPHS[char]
            
            # Loop through the 5 vertical rows
            for row_idx, row_string in enumerate(matrix):
                # Loop through the 3 horizontal columns
                for col_idx, bit in enumerate(row_string):
                    if bit == '1':
                        # Calculate exact block position
                        bx = current_x + (col_idx * block_size)
                        by = start_y + (row_idx * block_size_y)
                        
                            
                        pygame.draw.rect(surface, color, (bx, by, block_size, block_size_y))
                        
        # Space out the next digit (3 columns + 1 blank column for spacing)
        current_x += 4 * block_size

# Generates a pure retro arcade square wave sound sample
def generate_square_wave(frequency, duration_secs=0.05, volume=0.3):
    
    sample_rate = 44100
    num_samples = int(sample_rate * duration_secs)
    
    # Calculate the period of the wave in samples
    period = sample_rate / frequency
    
    # Create a time array
    t = np.arange(num_samples)
    
    # Generate square wave: +1 when the cycle is in the first half, -1 in the second half
    # Scale to 16-bit signed integer max range (32767)
    wave = 32767 * np.sign(np.sin(2 * np.pi * frequency * t / sample_rate))
    
    # Apply volume adjustment
    wave = (wave * volume).astype(np.int16)
    
    # Return as a Pygame Sound object
    return pygame.mixer.Sound(buffer=wave)

# note frequencies
N_C5 = 523.25

N_Db5 = 554.37
N_D5 = 587.33
N_Eb5 = 622.25
N_E5 = 659.26
N_F5 = 698.46
N_Gb5 = 749.99
N_G5 = 783.99
N_Ab5 = 830.60
N_A5 = 880.0
N_Bb5 = 932.33
N_B5 = 987.77


N_C6 = 1046.5
N_Db6 = 1108.73
N_D6 = 1174.66
N_Eb6 = 1244.51
N_E6 = 1318.51
N_F6 = 1396.61
N_Gb6 = 1479.98
N_G6 = 1569.98
N_Ab6 = 1661.22
N_A6 = 1760.9
N_Bb6 = 1864.66
N_B6 = 1975.53
N_C7 = 2093.0

sound_wall = generate_square_wave(N_C6, duration_secs=0.01)        
sound_paddle = generate_square_wave(N_C7, duration_secs=0.012)

sound_C5 = generate_square_wave(N_C5, duration_secs=0.008)
sound_Db5 = generate_square_wave(N_Db5, duration_secs=0.008)
sound_D5 = generate_square_wave(N_D5, duration_secs=0.008)
sound_Eb5 = generate_square_wave(N_Eb5, duration_secs=0.008)
sound_E5 = generate_square_wave(N_E5, duration_secs=0.008)
sound_F5 = generate_square_wave(N_F5, duration_secs=0.008)
sound_Gb5 = generate_square_wave(N_Gb5, duration_secs=0.008)
sound_G5 = generate_square_wave(N_G5, duration_secs=0.008)
sound_Ab5 = generate_square_wave(N_Ab5, duration_secs=0.008)
sound_A5 = generate_square_wave(N_A5, duration_secs=0.008)
sound_Bb5 = generate_square_wave(N_Bb5, duration_secs=0.008)
sound_B5 = generate_square_wave(N_B5, duration_secs=0.008)
sound_C6 = generate_square_wave(N_C6, duration_secs=0.008)

soundscales = {
    'MAJOR': [sound_C5, sound_C5, sound_E5, sound_E5, sound_G5, sound_G5, sound_C6, sound_C6],
    'MINOR': [sound_C5, sound_C5, sound_Eb5, sound_Eb5, sound_G5, sound_G5, sound_C6, sound_C6],
    'ROCK': [sound_E5, sound_E5, sound_G5, sound_G5, sound_A5, sound_A5, sound_Bb5, sound_Bb5],
    'BLUES': [sound_Eb5, sound_Eb5, sound_G5, sound_G5, sound_A5, sound_A5, sound_Bb5, sound_Bb5],
    'PENTATONIC': [sound_D5, sound_D5, sound_E5, sound_E5, sound_G5, sound_G5, sound_A5, sound_A5],
    'FULL MAJOR': [sound_C5, sound_D5, sound_E5, sound_F5, sound_G5, sound_A5, sound_B5, sound_C6],
    'RANDOM': [sound_C5, sound_Db5, sound_D5, sound_Eb5, sound_E5, sound_F5, sound_Gb5, sound_G5, sound_Ab5, sound_A5, sound_Bb5, sound_B5, sound_C6],
    'MONOTONIC': [sound_C5, sound_C5, sound_C5, sound_C5, sound_C5, sound_C5, sound_C5, sound_C5],
}

soundscaleindex = 7         # (new) default is monotonic

# dur'ish (major)
if '-major ' in cmdline:
    soundscaleindex = 0


# moll'ish (minor)
if '-minor ' in cmdline:
    soundscaleindex = 1

# rock'ish
if '-rock ' in cmdline:
    soundscaleindex = 2

# blues'ish
if '-blues ' in cmdline:
    soundscaleindex = 3

# pentatonic
if '-penta ' in cmdline or '-pentatonic ' in cmdline:
    soundscaleindex = 4

# pentatonic
if '-fullscale ' in cmdline or '-fullmajor ' in cmdline:
    soundscaleindex = 5

if '-random ' in cmdline or '-randomscale ' in cmdline:
    soundscaleindex = 6

if '-monotonic ' in cmdline:
    soundscaleindex = 7


soundscale = list(soundscales)[soundscaleindex]



def drawSoftRect(surface, w, h, color, rounded = False):
    daacolor = (color[0]//2, color[1]//2, color[2]//2)
    if not rounded:
        pygame.draw.rect(surface, daacolor, [0, 0, w, h])
    else:
        pygame.draw.rect(surface, daacolor, [0, 1, w, w])
        pygame.draw.rect(surface, daacolor, [1, 0, h-2, h])
        
    pygame.draw.rect(surface, color, [1, 1, w-2, h-2])
    


class Brick(pygame.sprite.Sprite):
    def __init__(self, color, x, y, value, row):
        super().__init__()
        self.image = pygame.Surface([BRICK_WIDTH, BRICK_HEIGHT])
        self.drawcolor = GREY if nocolorstrips else color
        self.point_value = value
        self.color = color
        self.row = row
        self.rect = self.image.get_rect()
        drawSoftRect(self.image, self.rect.width, self.rect.height, self.drawcolor)
        self.rect.x = x
        self.rect.y = y


class Paddle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface([PADDLE_WIDTH, PADDLE_HEIGHT])
        self.rect = self.image.get_rect()
        self.paddle_shrunk = False
        self.original_width = self.rect.width
        drawSoftRect(self.image, self.rect.width, self.rect.height, self.color)
    
    def grow(self):
        if self.paddle_shrunk:
            old_center = self.rect.center
            self.image = pygame.transform.scale(paddle.image, (self.original_width, self.rect.height))
            self.paddle_shrunk = False
            self.rect.width = self.original_width
            self.rect.center = old_center                    
            drawSoftRect(self.image, self.rect.width, self.rect.height, self.color)

    def shrink(self):
        if not self.paddle_shrunk:
            old_center = self.rect.center
            self.image = pygame.transform.scale(paddle.image, (self.original_width//2, self.rect.height))
            self.paddle_shrunk = True
            self.rect.width = self.original_width // 2
            self.rect.center = old_center                    
            drawSoftRect(self.image, self.rect.width, self.rect.height, self.color)


class Ball(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.image = pygame.Surface([BALL_WIDTH, BALL_HEIGHT])
        self.rect = self.image.get_rect()
        self.velocity = initial_ball_speed()
        self.color = (-1,-1,-1)
        self.roundball = not authentic
        self.setcolor(color)
    
    def setcolor(self, color):
        if color != self.color:
            self.color = color
            drawSoftRect(self.image, self.rect.width, self.rect.height, self.color, True)
        
    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]


# quick and dirty class for reading joysticks
# good thing is that it works in pygame 1 and 2
class Joystick:
    def __init__(self):
        self.move = pygame.math.Vector2(0,0)
        self.buttons = []
        pygame.joystick.init()
        self.numsticks = pygame.joystick.get_count()
        # stick names can be used for detecting stick properties
        self.sticknames = []
        for i in range(self.numsticks):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            name = joystick.get_name()
            self.sticknames.append(name)
        
    def get_joy(self):
        # Get count of joysticks (it may have changed? at least in pygame 2)
        joystick_count = pygame.joystick.get_count()
        self.move.x = 0
        self.move.y = 0
        self.buttons = []
        # For each joystick:
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            # get axes
            axes = joystick.get_numaxes()
            for ii in range(axes):
                axis = joystick.get_axis(ii)
                # support analog movement
                if axis:
                    if ii == 0:
                        self.move.x = axis
                    if ii == 1:
                        self.move.y = axis
            # get buttons
            numbuttons = joystick.get_numbuttons()
            for i in range(numbuttons):
                buttonval = joystick.get_button(i)
                if buttonval and not i in self.buttons:
                    self.buttons.append(i)



paddle = Paddle(GREY if nocolorstrips else BLUE)
paddle.rect.x = GAME_WIDTH // 2 - PADDLE_WIDTH // 2
paddle.rect.y = GAME_HEIGHT - PADDLE_Y_FROM_BOTTOM - 11

ball = Ball(WHITE)

ball_list = pygame.sprite.Group()
paddle_list = pygame.sprite.Group()

ball_list.add(ball)
paddle_list.add(paddle)


all_bricks = pygame.sprite.Group()


def save_current_player_bricks(p_num):
    # save current player's bricks before next player turn
    player_data[p_num]["bricks_state"] = []

    for brick in all_bricks:
        # save all needed brick data as tuple
        player_data[p_num]["bricks_state"].append((brick.color, brick.rect.x, brick.rect.y, brick.point_value, brick.row))

def load_next_player_bricks(p_num):
    # load next player's bricks back to screen
    all_bricks.empty()
    
    # if player's first turn, create new full wall
    if not player_data[p_num]["bricks_state"]:
        rebuild_brick_wall()
    else:
        # reconstruct bricks from saved data
        for color, x, y, point_value, row in player_data[p_num]["bricks_state"]:
            # fix the colors (in case rainbowcolors or greyscale is used)
            # (point value is always tied with certain color band/strip)
            if point_value == 7:
                color = RED
            elif point_value == 5:
                color = ORANGE
            elif point_value == 3:
                color = GREEN
            else:
                color = YELLOW
            y = TOP_OFFSET + BRICKS_TOP + row * (Y_GAP + BRICK_HEIGHT)
            new_brick = Brick(color, x, y, point_value, row)
            all_bricks.add(new_brick)

def handle_ball_lost():
    global current_player, game_state, is_two_player
    
    p = current_player
    player_data[p]["lives"] -= 1
    
    if is_two_player:
        # check, if the other player has lives left
        next_player = 2 if current_player == 1 else 1
        
        if player_data[next_player]["lives"] > 0:
            # save current player's wall and load next's
            save_current_player_bricks(current_player)
            current_player = next_player
            load_next_player_bricks(current_player)
            
            # restore paddle state
            reset_ball_with_serve_wait()
            return
            
        # next player had no lives, but current still has:
        elif player_data[current_player]["lives"] > 0:
            # this player's turn continues with next ball
            reset_ball_with_serve_wait()
            return
    else:
        # 1-player game continues, if lives left
        if player_data[1]["lives"] > 0:
            reset_ball_with_serve_wait()
            return

    # game over, save game data so it can be restored on next launch
    save_game_data()

    reset_to_attract()




def rebuild_brick_wall():
    global all_bricks, wallshift
    # remove old bricks
    all_bricks.empty()
    # create new bricks, 8 rows, 14 columns
    for j in range(8):
        for i in range(14):
            n = j // 2        # j // 2 == color strip number 0(RED) - 3
            pts = 7 - n * 2   # 7, 5, 3, 1
            c = [RED,ORANGE,GREEN,YELLOW][n]
            brick = Brick(c, wallshift+WALL_WIDTH + i * (BRICK_WIDTH + X_GAP) - 4, TOP_OFFSET + BRICKS_TOP + j * (Y_GAP + BRICK_HEIGHT), pts, j)
            all_bricks.add(brick)
            

if not aiplay:
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True) 


def main():
    global game_state, all_bricks, serve_delay_timer, waiting_for_serve, fullfps, soundscale, soundscaleindex, soundscale_visible

    sfx_channel = pygame.mixer.Channel(0) 
    joysticks = Joystick()
    
    clock = pygame.time.Clock()
    run = True
    paused = False
    
    reset_to_attract()

    ai_target = 0
    current_time = pygame.time.get_ticks()
    starttext_visible = current_time + STARTTEXT_DELAY
    
    if dooverlay:
        WIN_W, WIN_H = dascreen.get_size()
        
        # game surface to middle of the screen
        OFFSET_X = (OVERLAY_W - GAME_WIDTH) // 2
        OFFSET_Y = (OVERLAY_H - GAME_HEIGHT) // 2
        dascreen.fill(BLACK)
        dascreen.blit(overlay, (-(OVERLAY_W-WIN_W)//2, -(OVERLAY_H-WIN_H)//2))
        pygame.display.flip()    # update whole screen at start

    while run:
        # get events, first joystick (using class)
        joysticks.get_joy()
        if len(joysticks.buttons):
            # upper buttons (including start & select, hopefully):
            for j in range(6,15):
                if j in joysticks.buttons:
                    run = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_c or event.key == pygame.K_RETURN) and pygame.key.get_mods() & pygame.KMOD_CTRL:
                run = False

            # pausing
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                if paused:
                    paused = False
                elif not nopause and game_state == "PLAYING":
                    paused = True
                    
            # switch to next sound scale
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s and not noscaleswitch:
                soundscaleindex = (soundscaleindex + (1 if not (pygame.key.get_mods() & pygame.KMOD_SHIFT) else -1)) % len(list(soundscales))
                soundscale = list(soundscales)[soundscaleindex]
                soundscale_visible = pygame.time.get_ticks() + 900

            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                fullfps = not fullfps


            if game_state == "PLAYING" and waiting_for_serve and not paused:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or event.type == pygame.MOUSEBUTTONDOWN or len(joysticks.buttons):
                    # Player pressed "serve ball" button
                    waiting_for_serve = False
                    
                    # start serve delay timer
                    serve_delay_timer = pygame.time.get_ticks() + get_serve_delay()

            # select 1 or 2 player game in attract mode
            if game_state == "ATTRACT":
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_1 or event.key == pygame.K_SPACE or event.key == pygame.K_RETURN) or event.type == pygame.MOUSEBUTTONDOWN or len(joysticks.buttons):
                    # start a 1-player game
                    start_new_game(two_player_mode=False)
                    
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                    # start a 2-player game
                    start_new_game(two_player_mode=True)
                        

        # update game logic
        current_time = pygame.time.get_ticks()
        
        # Toggle visibility every 180ms
        # (current_time // 180) increments every 180ms. 
        # Using % 2 creates a steady alternating True/False cycle.
        if (current_time // (360 if easyblink else 180)) % 2 == 0 and game_state == 'PLAYING' and not paused:
            score_visible = False
        else:
            score_visible = True
            
        # Blink serve light every 250ms (500 ms cycle)
        if ((current_time // 500) % 2 == 0 or game_state != 'PLAYING' or not waiting_for_serve) and not paused:
            serve_light_visible = False
        else:
            serve_light_visible = True
            

        if game_state in ["ATTRACT", "PLAYING"]:

            if game_state == "PLAYING" and not paused:
                # joystick input
                if joysticks.move.x:            # -1...1
                    paddle.rect.x += joysticks.move.x * PADDLE_SPEED
                
                # Handle Keyboard Inputs (Changes position by a fixed step)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    paddle.rect.x -= PADDLE_SPEED
                if keys[pygame.K_RIGHT]:
                    paddle.rect.x += PADDLE_SPEED
                # Handle Mouse Inputs (Changes position by relative movement)
                # get_rel() returns (delta_x, delta_y) since the last time it was called
                if not aiplay:
                    mouse_dx, mouse_dy = pygame.mouse.get_rel()
                    paddle.rect.x += mouse_dx
            
            if aiplay and not ball.rect.colliderect(paddle.rect) and ball.rect.bottom >= paddle.rect.top:
                ai_target = 0
            
            if (game_state == "ATTRACT" or aiplay) and not paused:
                if ball.rect.centery > GAME_HEIGHT * 0.50 and ball.velocity[1] > 0:
                    AI_SPEED = PADDLE_SPEED + 2 # max speed per frame
                elif ball.rect.centery > GAME_HEIGHT * 0.40 and ball.velocity[1] > 0:
                    AI_SPEED = PADDLE_SPEED - 2
                elif ball.rect.centery > GAME_HEIGHT * 0.30:
                    AI_SPEED = PADDLE_SPEED / 2
                else:
                    AI_SPEED = 0
                if ball.rect.centery > GAME_HEIGHT * 0.60 and ball.velocity[1] < 0:
                    AI_SPEED = 0

                # calculate distance between ball and paddle centers
                distance = ball.rect.centerx + ai_target - paddle.rect.centerx

                if abs(distance) < AI_SPEED:
                    paddle.rect.centerx = ball.rect.centerx + ai_target
                else:
                    # use full speed. np.sign(distance) returns -1 or 1 (or 0)
                    paddle.rect.x += int(np.sign(distance) * AI_SPEED)
            # Prevent Paddle From Leaving Screen Boundaries
            # original let the paddle go a little bit inside the wall, so do we:
            if paddle.rect.left < WALL_WIDTH // 2:
                paddle.rect.left = WALL_WIDTH // 2
            if paddle.rect.right > GAME_WIDTH - WALL_WIDTH // 2:
                paddle.rect.right = GAME_WIDTH - WALL_WIDTH // 2

            # check, if serve delay timer is on
            if serve_delay_timer > 0:
                if current_time >= serve_delay_timer:
                    # delay is over. get initial ball speed, random
                    ball.velocity = initial_ball_speed()
                    serve_delay_timer = 0
                # else delay is still on, do nothing

            if not paused:
                if not waiting_for_serve and serve_delay_timer == 0:
                    ball.update()
                
            if ball.rect.y < TOP_OFFSET + 38:
                ball.velocity[1] = abs(ball.velocity[1])
                if game_state == 'PLAYING':
                    if not player_data[current_player]["paddle_shrunk"]:
                        player_data[current_player]["paddle_shrunk"] = True
                        # Halve the paddle width
                        paddle.shrink()
                    
                    sfx_channel.play(sound_wall)

            if ball.rect.x >= GAME_WIDTH - WALL_WIDTH - 10:
                ball.velocity[0] = -abs(ball.velocity[0])
                if game_state == 'PLAYING':
                    sfx_channel.play(sound_wall)

            if ball.rect.x <= WALL_WIDTH:
                ball.velocity[0] = abs(ball.velocity[0])
                if game_state == 'PLAYING':
                    sfx_channel.play(sound_wall)

            # if ball missed:
            if game_state == 'PLAYING':
                if ball.rect.top > GAME_HEIGHT:
                    handle_ball_lost()

            if game_state == 'PLAYING':
                if ball.rect.colliderect(paddle.rect) and ball.velocity[1] > 0:
                    # 1. Force the strict, un-normalized vertical bounce flip
                    ball.velocity[1] = -abs(ball.velocity[1])  # Your standard Y velocity baseline
                    
                    # 2. Calculate the exact intersection ratio (0.0 to 1.0)
                    hit_position = (ball.rect.centerx - paddle.rect.x) / paddle.rect.width
                    
                    # 3. Apply the strict 1976 hardware horizontal speed steps
                    if hit_position < 0.25:
                        ball.velocity[0] = -6  # Far Left: Sharp shallow angle outward
                    elif hit_position < 0.50:
                        ball.velocity[0] = -3  # Inner Left: Soft vertical angle outward
                    elif hit_position < 0.75:
                        ball.velocity[0] = 3   # Inner Right: Soft vertical angle outward
                    else:
                        ball.velocity[0] = 6   # Far Right: Sharp shallow angle outward
                    
                    # when ai plays, vary the "hitting target point" like this, otherwise ai plays "too good"
                    if aiplay:
                        ai_target = random.randint(-paddle.rect.width//3, paddle.rect.width//3)
                        
                    if game_state == 'PLAYING':
                        sfx_channel.play(sound_paddle)
            if game_state == 'ATTRACT':
                if ball.rect.top >= GAME_HEIGHT - PADDLE_Y_FROM_BOTTOM - 16:
                    ball.velocity[1] = -abs(ball.velocity[1])
                    if not authentic:
                        # vary the x-velocity a bit so that attract mode bouncing is little more interesting
                        # subtle variation
                        ball.velocity[0] = math.copysign(random.randint(2,4), ball.velocity[0])
                    if game_state == 'PLAYING':
                        sfx_channel.play(sound_paddle)

            csize = 0
            collision_count = 0
            brick = None
            crow = -1
            if ball.velocity[1] < 0:
                crow = 8
            for b in all_bricks:
                if ball.rect.colliderect(b.rect):
                    collision_count += 1
                    ccsize = b.rect.clip(ball.rect).width * b.rect.clip(ball.rect).height
                    ccrow = b.row
                    # select brick, that is on the first row from the ball's direction, and the biggest collider on the same row
                    if ball.velocity[1] < 0 and ccrow < crow or ball.velocity[1] > 0 and ccrow > crow or ccrow == crow and ccsize > csize:
                        brick = b
                        crow = ccrow
                        csize = ccsize
                    
            collision_detected = False
            if collision_count:
                if game_state == 'PLAYING':
                    player_data[current_player]["score"] += brick.point_value
                    player_data[current_player]["hit_counter"] += 1
                    
                # Check row color for speed-up or paddle shrink
                # (Assuming brick.color holds the color tuple or name)
                if brick.color == RED or brick.color == ORANGE:
                    player_data[current_player]["highest_row_hit"] = True
                
                # Standard TTL Speed Step calculation
                # Base velocity is 4. We adjust the baseline dynamically:
                base_y_speed = 4
                if player_data[current_player]["hit_counter"] >= 4:
                    base_y_speed = 6  # Intermediate speed 1
                if player_data[current_player]["hit_counter"] >= 12:
                    base_y_speed = 8  # Intermediate speed 2
                if player_data[current_player]["highest_row_hit"] and game_state == 'PLAYING':
                    base_y_speed = 10  # Maximum speed
                

                # Apply the updated Y speed (preserving the current up/down direction)
                if ball.velocity[1] > 0:
                    ball.velocity[1] = base_y_speed
                else:
                    ball.velocity[1] = -base_y_speed

                # Handle standard bounce axis inversion
                overlap_x = min(ball.rect.right, brick.rect.right) - max(ball.rect.left, brick.rect.left)
                overlap_y = min(ball.rect.bottom, brick.rect.bottom) - max(ball.rect.top, brick.rect.top)

                # if we're hitting more than one brick, just back off!
                if collision_count > 1:
                    ball.velocity[0] *= -1
                    ball.velocity[1] *= -1
                elif overlap_x < overlap_y:
                    # --- side hit ---
                    # reverse direction only if ball is moving towards brick
                    if (ball.velocity[0] > 0 and ball.rect.centerx < brick.rect.centerx) or \
                       (ball.velocity[0] < 0 and ball.rect.centerx > brick.rect.centerx):
                        ball.velocity[0] *= -1
                else:
                    # --- top/bottom hit ---
                    # reverse direction only if ball is moving towards brick
                    if (ball.velocity[1] > 0 and ball.rect.centery < brick.rect.centery) or \
                       (ball.velocity[1] < 0 and ball.rect.centery > brick.rect.centery):
                        ball.velocity[1] *= -1
                    else:   # to be safe, back off
                        ball.velocity[0] *= -1
                        ball.velocity[1] *= -1
                
                # Trigger the correct pitch based on the point tier
                if game_state == 'PLAYING':
                    pitch = 7 - brick.row
                    if soundscaleindex == 6: # RANDOM
                        sfx_channel.play(random.choice(soundscales[soundscale]))
                    else:
                        sfx_channel.play(soundscales[soundscale][pitch])
                    brick.kill()
                    collision_detected = True

            if collision_detected:
                if len(all_bricks) == 0:
                    # wall played through. which wall?
                    if player_data[current_player]["current_wall"] == 1:
                        player_data[current_player]["current_wall"] = 2
                        rebuild_brick_wall()
                        waiting_for_serve = False  # no serve, game just continues
                        
                    elif player_data[current_player]["current_wall"] == 2:
                        if happyend:
                            if is_two_player:
                                # store empty bricks state
                                player_data[current_player]["bricks_state"] = []
                                # lives to zero (player has nothing to play anymore)
                                player_data[current_player]["lives"] = 0
                                # handle_ball_lost switches to another player, if lives left
                                handle_ball_lost()                        
                            else:
                                # one player end with happy end:
                                # go straight to attract, score _and_ ball number stays on screen
                                game_state = "ATTRACT"
                                # make the ball go slower
                                ball.velocity = [ball.velocity[0],  math.copysign(4, ball.velocity[0])]  # base speed 4
                                save_game_data()
                        else:
                            # traditional end: do nothing, no happy end. all lives must be lost before game ends
                            pass
                        

        # --- DRAWING
        # on the game area (screen)
        screen.fill(BLACK)
        
        all_bricks.draw(screen)
        if game_state == 'PLAYING':
            paddle_list.draw(screen)
        
        # borders
        pygame.draw.line(screen, GREY, [0, TOP_OFFSET + 19], [GAME_WIDTH, TOP_OFFSET + 19], 37)
        pygame.draw.line(screen, GREY, [(WALL_WIDTH / 2) - 1, 0], [(WALL_WIDTH / 2) - 1, GAME_HEIGHT], WALL_WIDTH)
        pygame.draw.line(screen, GREY, [(GAME_WIDTH - WALL_WIDTH / 2) - 1, 0], [(GAME_WIDTH - WALL_WIDTH / 2) - 1, GAME_HEIGHT], WALL_WIDTH)
        if not nocolorstrips:        
            # small fadeout
            for i in range(5):
                z=44*i+44
                pygame.draw.line(screen, (z,z,z), [0, GAME_HEIGHT-i-1], [WALL_WIDTH - 1, GAME_HEIGHT-i-1], 1)
                pygame.draw.line(screen, (z,z,z), [GAME_WIDTH - WALL_WIDTH, GAME_HEIGHT-i-1], [GAME_WIDTH - 1, GAME_HEIGHT-i-1], 1)
                pygame.draw.line(screen, (z,z,z), [0, i], [WALL_WIDTH - 1, i], 1)
                pygame.draw.line(screen, (z,z,z), [GAME_WIDTH - WALL_WIDTH, i], [GAME_WIDTH - 1, i], 1)

        if game_state != 'PLAYING':     # paddle area is solid blue wall
            pygame.draw.line(screen, GREY if nocolorstrips else BLUE, [(WALL_WIDTH / 2) - 1, GAME_HEIGHT - PADDLE_Y_FROM_BOTTOM - 11 + PADDLE_HEIGHT / 2],  [(GAME_WIDTH - WALL_WIDTH / 2) - 1, GAME_HEIGHT - PADDLE_Y_FROM_BOTTOM - 11 + PADDLE_HEIGHT / 2], PADDLE_HEIGHT+1)
            
        if not nocolorstrips:
            # 46 is the height of the blue color strip
            pygame.draw.line(screen, BLUE, [(WALL_WIDTH / 2) - 1, GAME_HEIGHT - PADDLE_Y_FROM_BOTTOM - 11 + PADDLE_HEIGHT / 2 - 46 / 2], [(WALL_WIDTH / 2) - 1, GAME_HEIGHT - PADDLE_Y_FROM_BOTTOM - 11 + PADDLE_HEIGHT / 2 - 46 / 2 + 46], WALL_WIDTH)
            pygame.draw.line(screen, BLUE, [(GAME_WIDTH - WALL_WIDTH / 2) - 1, GAME_HEIGHT - PADDLE_Y_FROM_BOTTOM - 11 + PADDLE_HEIGHT / 2 - 46 / 2], [(GAME_WIDTH - WALL_WIDTH / 2) - 1, GAME_HEIGHT - PADDLE_Y_FROM_BOTTOM - 11 + PADDLE_HEIGHT / 2 - 46 / 2 + 46], WALL_WIDTH)

        if not nocolorstrips:
            pygame.draw.line(screen, RED, [(WALL_WIDTH / 2) - 1, TOP_OFFSET + BRICKS_TOP - 2.5], [(WALL_WIDTH / 2) - 1, TOP_OFFSET + BRICKS_TOP - 2.5 + 2 * BRICK_HEIGHT + 2 * Y_GAP], WALL_WIDTH)
            pygame.draw.line(screen, RED, [(GAME_WIDTH - WALL_WIDTH / 2) - 1, TOP_OFFSET + BRICKS_TOP - 2.5], [(GAME_WIDTH - WALL_WIDTH / 2) - 1, TOP_OFFSET + BRICKS_TOP - 2.5 + 2 * (BRICK_HEIGHT + Y_GAP)], WALL_WIDTH)

            pygame.draw.line(screen, ORANGE, [(WALL_WIDTH / 2) - 1, TOP_OFFSET + BRICKS_TOP - 2.5 + 2 * (BRICK_HEIGHT + Y_GAP)], [(WALL_WIDTH / 2) - 1, TOP_OFFSET + BRICKS_TOP - 2.5 + 4 * BRICK_HEIGHT + 4 * Y_GAP], WALL_WIDTH)
            pygame.draw.line(screen, ORANGE, [(GAME_WIDTH - WALL_WIDTH / 2) - 1, TOP_OFFSET + BRICKS_TOP - 2.5 + 2 * BRICK_HEIGHT + 2 * Y_GAP], [(GAME_WIDTH - WALL_WIDTH / 2) - 1, TOP_OFFSET + BRICKS_TOP - 2.5 + 4 * (BRICK_HEIGHT + Y_GAP)], WALL_WIDTH)

            pygame.draw.line(screen, GREEN, [(WALL_WIDTH / 2) - 1, TOP_OFFSET + BRICKS_TOP - 2.5 + 4 * BRICK_HEIGHT + 4 * Y_GAP], [(WALL_WIDTH / 2) - 1, TOP_OFFSET + BRICKS_TOP - 2.5 + 6 * BRICK_HEIGHT + 6 * Y_GAP], WALL_WIDTH)
            pygame.draw.line(screen, GREEN, [(GAME_WIDTH - WALL_WIDTH / 2) - 1, TOP_OFFSET + BRICKS_TOP - 2.5 + 4 * BRICK_HEIGHT + 4 * Y_GAP], [(GAME_WIDTH - WALL_WIDTH / 2) - 1, TOP_OFFSET + BRICKS_TOP - 2.5 + 6 * BRICK_HEIGHT + 6 * Y_GAP], WALL_WIDTH)

            pygame.draw.line(screen, YELLOW, [(WALL_WIDTH / 2) - 1, TOP_OFFSET + BRICKS_TOP - 2.5 + 6 * BRICK_HEIGHT + 6 * Y_GAP], [(WALL_WIDTH / 2) - 1, TOP_OFFSET + BRICKS_TOP - 2.5 + 8 * BRICK_HEIGHT + 8 * Y_GAP], WALL_WIDTH)
            pygame.draw.line(screen, YELLOW, [(GAME_WIDTH - WALL_WIDTH / 2) - 1, TOP_OFFSET + BRICKS_TOP - 2.5 + 6 * BRICK_HEIGHT + 6 * Y_GAP], [(GAME_WIDTH - WALL_WIDTH / 2) - 1, TOP_OFFSET + BRICKS_TOP - 2.5 + 8 * BRICK_HEIGHT + 8 * Y_GAP], WALL_WIDTH)
        

        # draw blinking score etc
        current_score1 = player_data[1]["score"]
        current_score2 = player_data[2]["score"]
        player1_score_text = f"{current_score1:03d}"            
        player2_score_text = f"{current_score2:03d}"            
        
        bsize = 12
        gap = 6 if fontgap else 0
        # P1 score
        if easyblink:
            draw_retro_glyphs(screen, player1_score_text, start_x=61+gap, start_y=TOP_OFFSET + 110 + gap // 2, block_size=bsize, color=DARKGREY)
        if score_visible or current_player == 2:
            draw_retro_glyphs(screen, player1_score_text, start_x=61+gap, start_y=TOP_OFFSET + 110 + gap // 2, block_size=bsize)
        # P2 score
        if easyblink:
            draw_retro_glyphs(screen, player2_score_text, start_x=(GAME_WIDTH-WALL_WIDTH)//2+62+gap + 48, start_y=TOP_OFFSET + 110 + gap // 2, block_size=bsize, color=DARKGREY)
        if score_visible or current_player == 1:
            draw_retro_glyphs(screen, player2_score_text, start_x=(GAME_WIDTH-WALL_WIDTH)//2+62+gap + 48, start_y=TOP_OFFSET + 110 + gap // 2, block_size=bsize)
        # current player
        draw_retro_glyphs(screen, str(current_player), start_x=WALL_WIDTH+gap - 1, start_y=TOP_OFFSET + 38+gap, block_size=bsize)
        # current ball
        ballno = 4 - player_data[current_player]["lives"]
        draw_retro_glyphs(screen, str(ballno), start_x=(GAME_WIDTH-WALL_WIDTH)//2+WALL_WIDTH+gap + 48, start_y=TOP_OFFSET + 38+gap, block_size=bsize)

        if not waiting_for_serve and serve_delay_timer == 0:
            # color the ball depenging on y position
            if ball.rect.centery > TOP_OFFSET + BRICKS_TOP and ball.rect.centery <= TOP_OFFSET + BRICKS_TOP + 2 * (Y_GAP + BRICK_HEIGHT):
                ball_color = RED
            elif ball.rect.centery > TOP_OFFSET + BRICKS_TOP + 2 * (Y_GAP + BRICK_HEIGHT) and ball.rect.centery <= TOP_OFFSET + BRICKS_TOP + 4 * (Y_GAP + BRICK_HEIGHT):
                ball_color = ORANGE
            elif ball.rect.centery > TOP_OFFSET + BRICKS_TOP + 4 * (Y_GAP + BRICK_HEIGHT) and ball.rect.centery <= TOP_OFFSET + BRICKS_TOP + 6 * (Y_GAP + BRICK_HEIGHT):
                ball_color = GREEN
            elif ball.rect.centery > TOP_OFFSET + BRICKS_TOP + 6 * (Y_GAP + BRICK_HEIGHT) and ball.rect.centery <= TOP_OFFSET + BRICKS_TOP + 8 * (Y_GAP + BRICK_HEIGHT):
                ball_color = YELLOW
            elif ball.rect.centery > GAME_HEIGHT - PADDLE_Y_FROM_BOTTOM - 11 + PADDLE_HEIGHT / 2 - 46 / 2 and ball.rect.centery <= GAME_HEIGHT - PADDLE_Y_FROM_BOTTOM - 11 + PADDLE_HEIGHT / 2 - 46 / 2 + 46:
                ball_color = BLUE
            else:
                ball_color = WHITE
            if nocolorstrips:
                ball_color = WHITE

            # update ball's color and draw it
            #ball.image.fill(ball_color)            
            ball.setcolor(ball_color)
            ball_list.draw(screen)
            
        if game_state == "PLAYING" and waiting_for_serve and doservelight and serve_light_visible:
            draw_retro_glyphs(screen, "SERVE", GAME_WIDTH - 82 - WALL_WIDTH, TOP_OFFSET+9, 4, color=BLACK if nocolorstrips else RED)

        if paused:
            draw_retro_glyphs(screen, "PAUSED", WALL_WIDTH + 6, TOP_OFFSET+9, 4, color=BLACK if nocolorstrips else RED)

        if soundscale_visible:
            if not authentic:
                draw_retro_glyphs(screen, "SOUNDSCALE: "+soundscale, GAME_WIDTH // 2, TOP_OFFSET+9, 4, color=BLACK if nocolorstrips else BLUE, centerx = True)
            if current_time >= soundscale_visible:
                soundscale_visible = 0

        if starttext_visible:
            if not authentic:
                draw_retro_glyphs(screen, STARTTEXT, GAME_WIDTH // 2, TOP_OFFSET+(GAME_HEIGHT - PADDLE_Y_FROM_BOTTOM - TOP_OFFSET) // 2, 4, color=WHITE, centerx = True)
            if current_time >= starttext_visible:
                starttext_visible = 0


        if dotextoverlay:
            screen.blit(textoverlay, (WALL_WIDTH + 46, TOP_OFFSET + 83))

        WIN_W, WIN_H = dascreen.get_size()
        GAME_W = GAME_WIDTH
        GAME_H = GAME_HEIGHT

        if not fullscreen and not overlay:
            dascreen.fill(BLACK)
        
        scr = screen
        if mini:
            GAME_W = GAME_WIDTH // 2
            GAME_H = GAME_HEIGHT // 2
            scr = pygame.transform.scale(screen, (GAME_W, GAME_H))
        if micro:
            GAME_W = GAME_WIDTH // 2.5
            GAME_H = GAME_HEIGHT // 2.5
            scr = pygame.transform.scale(screen, (GAME_W, GAME_H))
            
        # game surface to middle of the screen
        OFFSET_X = (OVERLAY_W - GAME_W) // 2
        OFFSET_Y = (OVERLAY_H - GAME_H) // 2

        if overlayname == 'breakouta':
            OFFSET_Y += 50
            
        # center it in the window
        dascreen.blit(scr, (OFFSET_X - (OVERLAY_W-WIN_W)//2, OFFSET_Y - (OVERLAY_H-WIN_H)//2))   # working
        if not fullscreen:
            pygame.display.flip()   # update all, because user can resize the window
        else:
            if overlayname == 'breakouta':
                dascreen.blit(overlay, (-(OVERLAY_W-WIN_W)//2, -(OVERLAY_H-WIN_H)//2))
            pygame.display.update(screen.get_rect().move((OFFSET_X - (OVERLAY_W-WIN_W)//2, OFFSET_Y - (OVERLAY_H-WIN_H)//2)))
        if not fullfps:
            clock.tick(FPS)

    pygame.quit()


main()


