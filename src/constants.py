import sys

# Constants
SCREEN_SIZE = WIDTH, HEIGHT = 700, 700
GRID_X, GRID_Y = 50, 50
FPS = 60
FLT_MAX = sys.float_info.max

DEBUG_MODE = False

# https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


# Colors
WHITE = (255, 255, 255)
LIGHT_GREY = (240, 240, 240)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)

# https://colorhunt.co/palette/258165
LIGHT_GREEN = hex_to_rgb("c5d7bd")
DARKER_GREEN = hex_to_rgb("9fb8ad")
DARK_GREY = hex_to_rgb("383e56")
PASTEL_ORANGE = hex_to_rgb("fb743e")

# Color Settings
GRID_COLOR = WHITE
START_COLOR = GREEN
END_COLOR = RED
WALL_COLOR = BLACK

# A* Colors
OPEN_COLOR = GREEN
CLOSED_A_COLOR = DARK_GREY
PATH_COLOR = PASTEL_ORANGE

# Maze Colors
VISITED_COLOR = LIGHT_GREEN
CLOSED_MAZE_COLOR = DARKER_GREEN
