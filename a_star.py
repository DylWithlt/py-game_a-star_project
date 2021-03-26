import math
from queue import PriorityQueue

from constants import BLUE, PURPLE, FLT_MAX


def calculate_h(tile, end):
    return math.sqrt(math.pow(tile.pos['x'] - end.pos['x'], 2.0) + math.pow(tile.pos['y'] - end.pos['y'], 2.0))


class ASTAR:
    open_list = PriorityQueue()
    found_dest = False
    finished = False

    def __init__(self, start, end, grid):
        self.start = start
        self.end = end
        self.grid = grid

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
            check_tile = self.grid.get_tile(dst[0], dst[1])

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
