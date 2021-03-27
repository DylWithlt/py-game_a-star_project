import pygame

from constants import FLT_MAX,\
    GRID_COLOR, WALL_COLOR


class Tile(pygame.Surface):
    blocked = False
    closed = False
    base_color = GRID_COLOR
    color = GRID_COLOR
    rect = pygame.rect.Rect
    parent = None
    visited = False

    drag_clicked = False

    f = FLT_MAX
    h = FLT_MAX
    g = FLT_MAX

    def __init__(self, rect, pos):
        super().__init__(rect.size)

        self.base_color = None
        self.color = None
        self.rect = rect
        self.pos = pos

    def block(self, toggle):
        self.blocked = toggle
        self.set_color(toggle and WALL_COLOR or GRID_COLOR)

    def __gt__(self, other):
        return self.f > other.f

    def __lt__(self, other):
        return self.f < other.f

    def set_color(self, color):
        if self.pos["x"] % 2 != self.pos["y"] % 2:
            color = (round(color[0] * 0.9), round(color[1] * 0.9), round(color[2] * 0.9))

        if not self.base_color:
            self.base_color = color

        self.color = color
        self.fill(self.color)


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

                tile = Tile(pygame.rect.Rect(x * self.tile_width,
                                             y * self.tile_height,
                                             self.tile_width,
                                             self.tile_height),
                            {'x': x, 'y': y})

                tile.set_color(GRID_COLOR)

                self.tiles.append(tile)

    def get_tile(self, x, y):
        if not self.is_valid(x, y):
            return None

        for tile in self.tiles:
            if tile.pos['x'] == x and tile.pos['y'] == y:
                return tile
        return None

    def is_valid(self, x, y):
        return 0 <= x <= self.width and 0 <= y <= self.width
