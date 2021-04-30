import pygame

from board import Grid
from a_star import ASTAR
from maze import MazeGenerator
from constants import DEBUG_MODE, FPS, GRID_X, GRID_Y, SCREEN_SIZE,\
    GRID_COLOR, WALL_COLOR, START_COLOR, END_COLOR,\
    BLACK, WHITE

# Initialize pygame, create window.
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("A* Grid")
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 10)

print("----- Controls -----")
print("Left Click: place/remove wall")
print("Right Click: place/remove start/end")
print("s to start A*")
print("f to toggle off step mode")
print("n to increment the step")
print("r to clear the board and restart")


def render(grid_instance):
    for tile in grid_instance.tiles:
        screen.blit(tile, tile.rect.topleft)
        if DEBUG_MODE:
            screen.blit(font.render("%0.2f" % (tile.f > 100 and 999 or tile.f),
                                    True, BLACK, WHITE), tile.rect.topleft)


def draw_screen(grid):
    screen.fill(BLACK)

    # draw the tile (a pygame surface) at the location based on the topleft of the rect
    # WIN.blit(green_tile, green_tile.rect.topleft)
    # WIN.blit(blue_tile, blue_tile.rect.topleft)

    render(grid)

    pygame.display.update()


def main():
    grid = Grid(GRID_X, GRID_Y, SCREEN_SIZE)
    grid.build_grid()

    a_star = None
    maze_generator = None
    step_a_on_update = True

    pressed_tiles = []

    running = True
    while running:
        # run the program at most 60 frames per second - makes program controllable on any system
        clock.tick(FPS)
        # process inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed(3) == (0, 0, 1):
                    # right mouse clicked
                    for tile in grid.tiles:
                        if tile.rect.collidepoint(event.pos):
                            if tile == grid.start_tile:
                                tile.set_color(GRID_COLOR)
                                grid.start_tile = None
                            elif tile == grid.end_tile:
                                tile.set_color(GRID_COLOR)
                                grid.end_tile = None
                            elif not tile.blocked:
                                if not grid.start_tile:
                                    tile.set_color(START_COLOR)
                                    grid.start_tile = tile
                                elif not grid.end_tile:
                                    tile.set_color(END_COLOR)
                                    grid.end_tile = tile

            elif event.type == pygame.MOUSEBUTTONUP:
                for tile in pressed_tiles:
                    if tile.drag_clicked:
                        tile.drag_clicked = False
                pressed_tiles.clear()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    if grid.start_tile and grid.end_tile:
                        a_star = ASTAR(grid.start_tile, grid.end_tile, grid)
                elif event.key == pygame.K_n:
                    if a_star:
                        a_star.step_a_star()
                elif event.key == pygame.K_f:
                    step_a_on_update = not step_a_on_update
                elif event.key == pygame.K_r:
                    grid = Grid(GRID_X, GRID_Y, SCREEN_SIZE)
                    grid.build_grid()
                elif event.key == pygame.K_m:
                    maze_generator = MazeGenerator(grid)

        # moved outside event loop for mouse drag
        # gets called while left mouse is held
        if pygame.mouse.get_pressed(3) == (1, 0, 0):
            for tile in grid.tiles:
                if tile.rect.collidepoint(pygame.mouse.get_pos()):
                    # if the tile is neither a start or end, and it hasn't been clicked during mouse down
                    if not (tile == grid.start_tile or tile == grid.end_tile) and not tile.drag_clicked:
                        tile.block(not tile.blocked)

                    # while mouse is held, change the tile
                    if not tile.drag_clicked:
                        pressed_tiles.append(tile)
                        tile.drag_clicked = True

        # update
        if step_a_on_update and a_star:
            if not a_star.finished:
                a_star.step_a_star()

        if maze_generator and not maze_generator.Finished:
            maze_generator.step_draw_maze()

        # render
        draw_screen(grid)

    pygame.quit()


if __name__ == "__main__":
    main()
