import pygame


class Tile(pygame.Surface):
    is_wall = False
    is_start = False
    is_end = False
    base_color = (0, 0, 0)
    color = (0, 0, 0)
    rect = pygame.rect.Rect
    location = []

    def __init__(self, color, rect, location):
        super().__init__(rect.size)

        self.base_color = color
        self.rect = rect
        self.location = location

        self.fill(color)

    def set_color(self, color):
        self.color = color
        self.fill(color)


class Grid:
    width, height = 0, 0
    tile_width, tile_height = 0, 0
    tile = Tile

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def build_grid(self, screen_size):
        """
        Build the grid of tiles.
        screen_size = tuple(screen_width, screen_height) in pixels
        """
        tiles = []
        color = (255, 255, 255)
        self.tile_width = int(screen_size[0] / self.width)
        self.tile_height = int(screen_size[1] / self.height)

        for j in range(self.height):
            for i in range(self.width):
                # alternate color of tiles to make grid visible
                # shift is to make rows alternate if given an even width and height
                if (self.width % 2 == 0 and self.height % 2 == 0) and j % 2 == 1:
                    shift = 1
                else:
                    shift = 0

                if (i + j * self.width) % 2 == shift:
                    color = (255, 255, 255)
                else:
                    color = (240, 240, 240)

                tiles.append(Tile(color,
                                  pygame.rect.Rect(i * self.tile_width,
                                                   j * self.tile_height,
                                                   self.tile_width,
                                                   self.tile_height),
                                  [i, j]))

        return tiles


pygame.init()

SIZE = WIDTH, HEIGHT = 500, 500

WIN = pygame.display.set_mode(SIZE)
pygame.display.set_caption("A* Grid")

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

grid = Grid(10, 10)
tiles = grid.build_grid(SIZE)

print("----- Controls -----")
print("Left Click: place/remove wall")
print("Right Click: place/remove start/end")


def draw_screen():
    WIN.fill(BLACK)

    # draw the tile (a pygame surface) at the location based on the topleft of the rect
    # WIN.blit(green_tile, green_tile.rect.topleft)
    # WIN.blit(blue_tile, blue_tile.rect.topleft)

    for tile in tiles:
        WIN.blit(tile, tile.rect.topleft)

    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    is_running = True
    have_placed_start = False
    have_placed_end = False
    while is_running:
        # run the program at most 60 frames per second - makes program controllable on any system
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed(3) == (1, 0, 0):
                    # left mouse button clicked
                    for tile in tiles:
                        if tile.rect.collidepoint(event.pos):
                            if tile.is_wall:
                                tile.set_color(tile.base_color)
                                tile.is_wall = False
                            else:
                                tile.set_color(BLACK)
                                tile.is_wall = True
                if pygame.mouse.get_pressed(3) == (0, 0, 1):
                    # right mouse clicked
                    for tile in tiles:
                        if tile.rect.collidepoint(event.pos):
                            if not have_placed_start and not tile.is_start and not tile.is_end:
                                tile.set_color(GREEN)
                                tile.is_start = True
                                have_placed_start = True
                            elif have_placed_start and tile.is_start:
                                tile.set_color(tile.base_color)
                                tile.is_start = False
                                have_placed_start = False
                            elif not have_placed_end and have_placed_start and not tile.is_end:
                                tile.set_color(RED)
                                tile.is_end = True
                                have_placed_end = True
                            elif have_placed_end and tile.is_end:
                                tile.set_color(tile.base_color)
                                tile.is_end = False
                                have_placed_end = False

        draw_screen()

    pygame.quit()


if __name__ == "__main__":
    main()
