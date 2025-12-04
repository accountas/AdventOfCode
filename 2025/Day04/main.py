from common.data import *
from common.grid import *

from copy import deepcopy


def can_be_reached(grid, roll):
    return list(grid.neighbour_values(roll, ALL_DIRECTIONS)).count("@") < 4


def maybe_remove(grid, point, propagate=True):
    if grid[point] == "@" and can_be_reached(grid, point):
        grid[point] = "x"
        if propagate:
            for point in grid.neighbours(point, ALL_DIRECTIONS):
                maybe_remove(grid, point)


def count_removed(grid, propagate):
    grid = deepcopy(grid)
    for point in grid.pos_iter():
        maybe_remove(grid, point, propagate)
    return len(grid.find("x"))


def main():
    grid = Grid.from_string(get_data(year=2025, day=4, sample=False))

    print("Part 1:", count_removed(grid, propagate=False))
    print("Part 2:", count_removed(grid, propagate=True))


if __name__ == "__main__":
    main()
