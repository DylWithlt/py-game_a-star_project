import random

from constants import GRID_COLOR, VISITED_COLOR, CLOSED_MAZE_COLOR


class MazeGenerator:

    def __init__(self, grid):
        self.grid = grid
        self.Finished = False
        self.stack = []

        # prepare grid
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                tile = self.grid.get_tile(x, y)

                if not (x % 2 == 1 and y % 2 == 1) and \
                        (x != self.grid.width - 1 and y != self.grid.height - 1):
                    tile.block(True)

        initial_tile = self.grid.get_tile(1, 1)
        initial_tile.visited = True
        self.stack.append(initial_tile)

    def step_draw_maze(self):
        if len(self.stack) <= 0:
            print("Maze draw done!")

            for tile in self.grid.tiles:
                if not tile.blocked:
                    tile.set_color(GRID_COLOR)

            self.Finished = True
            return

        current_tile = self.stack.pop()
        current_tile.set_color(VISITED_COLOR)

        # (x, y - 1) N
        # (x + 1, y) E
        # (x, y + 1) S
        # (x - 1, y) W
        directions = [
            (current_tile.pos["x"], current_tile.pos["y"] - 2, (0, 1)),
            (current_tile.pos["x"] + 2, current_tile.pos["y"], (-1, 0)),
            (current_tile.pos["x"], current_tile.pos["y"] + 2, (0, -1)),
            (current_tile.pos["x"] - 2, current_tile.pos["y"], (1, 0)),
        ]

        unvisited_neighbors = []
        for direction in directions:
            tile = self.grid.get_tile(direction[0], direction[1])
            if tile and not tile.visited and \
                    tile.pos["x"] < self.grid.width - 1 and tile.pos["y"] < self.grid.height - 1:
                unvisited_neighbors.append((direction, tile))

        if len(unvisited_neighbors) > 0:
            self.stack.append(current_tile)

            neighbor = random.choice(unvisited_neighbors)
            neighbor_tile = neighbor[1]
            neighbor_direction = neighbor[0]
            wall = self.grid.get_tile(neighbor_tile.pos["x"] + neighbor_direction[2][0],
                                      neighbor_tile.pos["y"] + neighbor_direction[2][1])
            if wall:
                wall.block(False)

            neighbor_tile.visited = True
            self.stack.append(neighbor_tile)
        else:
            current_tile.set_color(CLOSED_MAZE_COLOR)
