import pygame

from src.constants import FLT_MAX, DEBUG_MODE, BLACK, WHITE, LIGHT_GREY


class Tile(pygame.Surface):
    blocked = False
    closed = False
    base_color = BLACK
    color = WHITE
    rect = pygame.rect.Rect
    parent = None

    drag_clicked = False

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
    def __init__(self, width, height, screen_size):
        self.width = width
        self.height = height
        self.screen_size = screen_size

        self.tile_width = int(self.screen_size[0] / self.width)
        self.tile_height = int(self.screen_size[1] / self.height)
        self.tiles = []

        self.start_tile = None
        self.end_tile = None

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

    def get_tile(self, x, y):
        if not self.is_valid(x, y):
            return None

        for tile in self.tiles:
            if tile.pos['x'] == x and tile.pos['y'] == y:
                return tile
        return None

    def is_valid(self, x, y):
        return 0 <= x <= self.width and 0 <= y <= self.width
