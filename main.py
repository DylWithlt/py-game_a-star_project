import pygame

# Constants
SIZE = WIDTH, HEIGHT = 500, 500
FPS = 60

# Colors
WHITE = (255, 255, 255)
LIGHT_GREY = (240, 240, 240)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)


class Tile(pygame.Surface):
    is_wall = False
    base_color = BLACK
    color = WHITE
    rect = pygame.rect.Rect
    location = []

    def __init__(self, color, rect, location):
        super().__init__(rect.size)

        self.base_color = color
        self.color = color
        self.rect = rect
        self.location = location

        self.fill(color)

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
                                  [x, y]))

    def render(self):
        for tile in self.tiles:
            screen.blit(tile, tile.rect.topleft)


# Initialize pygame, create window.
pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("A* Grid")
clock = pygame.time.Clock()

grid = Grid(10, 10, SIZE)
grid.build_grid()

print("----- Controls -----")
print("Left Click: place/remove wall")
print("Right Click: place/remove start/end")


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
                            if tile.is_wall:
                                tile.set_color(tile.base_color)
                                tile.is_wall = False
                            else:
                                tile.set_color(BLACK)
                                tile.is_wall = True
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
                            else:
                                if not start_tile:
                                    tile.set_color(GREEN)
                                    start_tile = tile
                                elif not end_tile:
                                    tile.set_color(RED)
                                    end_tile = tile

        # update

        # render
        draw_screen()

    pygame.quit()


if __name__ == "__main__":
    main()
