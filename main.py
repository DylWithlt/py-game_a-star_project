import pygame
import sys
import math
from queue import PriorityQueue

# Constants
SIZE = WIDTH, HEIGHT = 700, 700
FPS = 120
FLT_MAX = sys.float_info.max

DEBUG_MODE = False

# Colors
WHITE = (255, 255, 255)
LIGHT_GREY = (240, 240, 240)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)


class Tile(pygame.Surface):
    blocked = False
    closed = False
    base_color = BLACK
    color = WHITE
    rect = pygame.rect.Rect
    parent = None

    f = FLT_MAX
    h = FLT_MAX
    g = FLT_MAX

    def __init__(self, color, rect, pos):
        super().__init__(rect.size)

        self.base_color = color
        self.color = color
        self.rect = rect
        self.pos = pos

        self.fill(color)

    def __gt__(self, other):
        return self.f > other.f

    def __lt__(self, other):
        return self.f < other.f

    def set_color(self, color):
        self.color = color
        self.fill(color)


class Grid:
    width, height = 0, 0
    tile_width, tile_height = 0, 0

    def __init__(self, width, height, screen_size):
        self.width = width
        self.height = height
        self.screen_size = screen_size

        self.tile_width = int(self.screen_size[0] / self.width)
        self.tile_height = int(self.screen_size[1] / self.height)
        self.tiles = []

    def build_grid(self):
        """
        Build the grid of tiles.
        """

        for x in range(self.height):
            for y in range(self.width):
                # alternate color of tiles to make grid visible
                # shift is to make rows alternate if given an even width and height

                color = LIGHT_GREY
                if x % 2 == y % 2:
                    color = WHITE

                self.tiles.append(Tile(color,
                                       pygame.rect.Rect(x * self.tile_width,
                                                        y * self.tile_height,
                                                        self.tile_width,
                                                        self.tile_height),
                                       {'x': x, 'y': y}))

    def render(self):
        for tile in self.tiles:
            screen.blit(tile, tile.rect.topleft)
            if DEBUG_MODE:
                screen.blit(font.render("%0.2f" % (tile.f > 100 and 999 or tile.f),
                                        True, BLACK, WHITE), tile.rect.topleft)

    def get_tile(self, x, y):
        if not self.is_valid(x, y):
            return None

        for tile in self.tiles:
            if tile.pos['x'] == x and tile.pos['y'] == y:
                return tile
        return None

    def is_valid(self, x, y):
        return 0 <= x <= self.width and 0 <= y <= self.width


# Initialize pygame, create window.
pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("A* Grid")
clock = pygame.time.Clock()

grid = Grid(50, 50, SIZE)
grid.build_grid()

font = pygame.font.Font('freesansbold.ttf', 10)

print("----- Controls -----")
print("Left Click: place/remove wall")
print("Right Click: place/remove start/end")


def calculate_h(tile, end):
    return math.sqrt(math.pow(tile.pos['x'] - end.pos['x'], 2.0) + math.pow(tile.pos['y'] - end.pos['y'], 2.0))


class ASTAR:
    open_list = PriorityQueue()
    found_dest = False
    finished = False

    def __init__(self, start, end):
        self.start = start
        self.end = end

        self.open_list.put(start)
        start.g = 0
        start.h = 0
        start.f = 0

    def step_a_star(self):
        if self.open_list.empty():
            print("No valid next step, path is impossible.")
            self.finished = True
            return

        if self.found_dest:
            print("Already found destination!")
            return

        # Remove current and move it to closed
        current = self.open_list.get()
        current.closed = True

        # Generate Successors
        # N.W  N  N.E
        #    \ | /
        # W -- C -- E
        #    / | \
        # S.W  S  S.E
        #
        # 0 C   -> Current    (x  , y)
        # 1 N   -> North      (x  , y-1)
        # 2 E   -> East       (x+1, y)
        # 3 S   -> South      (x  , y+1)
        # 4 W   -> West       (x-1, y)
        # 5 N.W -> North-West (x-1, y-1)
        # 6 N.E -> North-East (x+1, y-1)
        # 7 S.W -> South-West (x-1, y+1)
        # 8 S.E -> South-East (x+1, y+1)
        destinations = [
            (current.pos['x'], current.pos['y'] - 1),  # N
            (current.pos['x'] + 1, current.pos['y']),  # E
            (current.pos['x'], current.pos['y'] + 1),  # S
            (current.pos['x'] - 1, current.pos['y']),  # W
            (current.pos['x'] - 1, current.pos['y'] - 1),  # NW
            (current.pos['x'] + 1, current.pos['y'] - 1),  # NE
            (current.pos['x'] - 1, current.pos['y'] + 1),  # SW
            (current.pos['x'] + 1, current.pos['y'] + 1)  # SE
        ]

        for dst in destinations:
            check_tile = grid.get_tile(dst[0], dst[1])

            if not check_tile:
                continue

            if check_tile == self.end:
                check_tile.parent = current
                print("Reached goal!")
                nxt = check_tile
                check_tile.set_color(BLUE)
                while nxt.parent:
                    nxt = nxt.parent
                    nxt.set_color(BLUE)
                self.found_dest = True
                self.finished = True
                return
            elif not (check_tile.closed or check_tile.blocked):
                g_new = current.g + (check_tile.pos['x'] != current.pos['x'] and check_tile.pos['y'] != current.pos['y']
                                     and 1.5 or 1.0)

                h_new = calculate_h(check_tile, self.end)
                f_new = g_new + h_new

                if check_tile.f == FLT_MAX or check_tile.f > f_new:
                    self.open_list.put(check_tile)

                    check_tile.f = f_new
                    check_tile.g = g_new
                    check_tile.h = h_new
                    check_tile.parent = current
                    check_tile.set_color(PURPLE)


def draw_screen():
    screen.fill(BLACK)

    # draw the tile (a pygame surface) at the location based on the topleft of the rect
    # WIN.blit(green_tile, green_tile.rect.topleft)
    # WIN.blit(blue_tile, blue_tile.rect.topleft)

    grid.render()

    pygame.display.update()


def main():
    start_tile = None
    end_tile = None

    a_star = None
    step_a_on_update = False

    running = True
    while running:
        # run the program at most 60 frames per second - makes program controllable on any system
        clock.tick(FPS)

        # process inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed(3) == (1, 0, 0):
                    # left mouse button clicked
                    for tile in grid.tiles:
                        if tile.rect.collidepoint(event.pos):
                            if not (tile == start_tile or tile == end_tile):
                                if tile.blocked:
                                    tile.set_color(tile.base_color)
                                    tile.blocked = False
                                else:
                                    tile.set_color(BLACK)
                                    tile.blocked = True
                elif pygame.mouse.get_pressed(3) == (0, 0, 1):
                    # right mouse clicked
                    for tile in grid.tiles:
                        if tile.rect.collidepoint(event.pos):
                            if tile == start_tile:
                                tile.set_color(tile.base_color)
                                start_tile = None
                            elif tile == end_tile:
                                tile.set_color(tile.base_color)
                                end_tile = None
                            elif not tile.blocked:
                                if not start_tile:
                                    tile.set_color(GREEN)
                                    start_tile = tile
                                elif not end_tile:
                                    tile.set_color(RED)
                                    end_tile = tile
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    if start_tile and end_tile:
                        a_star = ASTAR(start_tile, end_tile)
                elif event.key == pygame.K_n:
                    if a_star:
                        a_star.step_a_star()
                elif event.key == pygame.K_r:
                    step_a_on_update = not step_a_on_update

        # update
        if step_a_on_update and a_star:
            if not a_star.finished:
                a_star.step_a_star()

        # render
        draw_screen()

    pygame.quit()


if __name__ == "__main__":
    main()
