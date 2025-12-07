from common.data import *
from common.grid import *
from common.point import *

from functools import cache


class QuantumManifold:
    def __init__(self, manifold: Grid):
        self._manifold = manifold

    @cache
    def num_ways_to_reach(self, pos: Point):
        if not self._manifold.is_valid(pos) or self._manifold[pos] == "^":
            return 0

        if self._manifold[pos] == "S":
            return 1

        total = self.num_ways_to_reach(pos + UP)

        for dir in [LEFT, RIGHT]:
            if self._manifold[pos + dir] == "^":
                total += self.num_ways_to_reach(pos + dir + UP)

        return total


def main():
    grid = Grid.from_string(get_data(year=2025, day=7, sample=False))
    width, height = grid.shape()

    manifold = QuantumManifold(grid)

    part_1 = sum(
        manifold.num_ways_to_reach(splitter + UP) > 0 
        for splitter in grid.find("^")
    )
    part_2 = sum(
        manifold.num_ways_to_reach(Point(height - 1, i))
        for i in range(width)
    )

    print("Part 1:", part_1)
    print("Part 2:", part_2)


if __name__ == "__main__":
    main()
