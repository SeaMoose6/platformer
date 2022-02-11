import pygame
import math
import random

pygame.init()

# constants
YELLOW = (219, 150, 31)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 77, 0)
BLOCK_COLOR = (252, 53, 3)

WIN_WIDTH = 800
WIN_HEIGHT = 600
TILE_SIZE = 50

#FONT = pygame.font.Font("assets/unifont.ttf", 25)
#BIG_FONT = pygame.font.Font("assets/unifont.ttf", 150)
PI = math.pi

DISPLAY_HEIGHT = 1000
DISPLAY_WIDTH = 1400
SIZE = (DISPLAY_WIDTH, DISPLAY_HEIGHT)


FPS = 120

TILE_SIZE = 50

LAYOUT = [
    '000000000000000000000000000000322222222222222222222222222223888888888888888888888888888889',
    '000000000000000000000000000000300000000000000000000000000003000000000000000000000000000009',
    '000000000000000000000000000000300000000000000000000000000003000000000000000000000000000009',
    '000000000000000000000000000000300000000000000000000000000003000000000000000000000000000009',
    '000000000000000000000000000000300000000000000001110000000003000000000000000000000000000009',
    '000000000000000000000000000000300000000000000000000000000003000000000000000000000000000009',
    '000000000000000000000000000000300000000000000000000000000003000000000000000006660000000009',
    '000000000000000000000000000000300000000111111100000000000050000000000000666000000000000009',
    '000000000000000000000000000000300000000000000000000000000000000000066600000000000000000009',
    '000000000000000000000000000000311000000000000000000011111113666000000000000000000000000009',
    '000000000000000000000000000000300110000000000000000000000003000000000000000000000000000009',
    '000000000000000000000000000000300000001110000000000000000003000000066600000000000000000009',
    '000000000000000000000000000000300000000000000000000000000003000000000000000000000000000009',
    '000000000000000000000000000000300000000000000001110000000003000000000000000000000000000009',
    '000000000000000000000000000000300000000000000110000000000003000000000000066600000000000009',
    '000000000000000000000000000000300011111110000000000000000003000000000000000000000000000009',
    '000000000000000000000000000000300000000000000000000000000003000000000000000000066600000009',
    '000000000000000000000000000000000400000000001100000000000003000000000000000000000000000009',
    '000000000000000000000000000000000000000000000000011110000003000000000000000000000000000009',
    '322222222222222222222222222222322222222222222222222222222223777777777777777777777777777779',

]
print(len('3222222222222222222232222222222222222222222222222322222222222222222223'))
print(len(LAYOUT)*50)



