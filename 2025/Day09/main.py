from common.data import *
from common.point import *
from common.grid import *
from common.utils import time_it
import itertools as it
from copy import deepcopy


def rectangle_area(p1: Point, p2: Point) -> int:
    return (abs(p1.x - p2.x) + 1) * (abs(p1.y - p2.y) + 1)


class CompressedPolygon:
    def __init__(self, points: list[Point]):
        self.points = points
        self.x_map = self._compress([p.x for p in points])
        self.y_map = self._compress([p.y for p in points])
        self.width = len(self.x_map)
        self.height = len(self.y_map)

        self.compressed_points = [
            Point(self.x_map[p.x], self.y_map[p.y]) for p in points
        ]
        self.compressed_grid = self._build_compressed_grid()
        self.prefix_sum = self._build_prefix_sum()

    def is_filled(self, p1: Point, p2: Point) -> bool:
        p1_compressed = Point(self.x_map[p1.x], self.y_map[p1.y])
        p2_compressed = Point(self.x_map[p2.x], self.y_map[p2.y])

        row1, row2 = sorted([p1_compressed.y, p2_compressed.y])
        col1, col2 = sorted([p1_compressed.x, p2_compressed.x])

        row2 -= 1
        col2 -= 1

        expected = rectangle_area(Point(col1, row1), Point(col2, row2))

        actual = (
            self.prefix_sum[row2 + 1, col2 + 1]
            - self.prefix_sum[row1, col2 + 1]
            - self.prefix_sum[row2 + 1, col1]
            + self.prefix_sum[row1, col1]
        )
        return actual == expected

    def print_compressed_grid(self, filled: chr = "#", empty: chr = "."):
        grid = deepcopy(self.compressed_grid)
        grid.values = grid.values[::-1]
        grid.map_values(lambda v: filled if v else empty)
        print(grid)

    def _compress(self, coords: list[int]) -> dict[int, int]:
        return {v: i for i, v in enumerate(sorted(set(coords)))}

    def _build_compressed_grid(self) -> Grid:
        polygon = self.compressed_points + [self.compressed_points[0]]

        # Mark vertical edges
        is_edge = set()
        for p1, p2 in it.pairwise(polygon):
            if p1.x == p2.x:
                y_start, y_end = sorted([p1.y, p2.y])
                for y in range(y_start, y_end):
                    is_edge.add((y, p1.x))

        # Fill in the grid
        compressed_grid = Grid.empty(self.height, self.width, False)
        for row in range(self.height):
            saw_odd_edges = False
            for col in range(self.width):
                saw_odd_edges ^= (row, col) in is_edge
                compressed_grid[row, col] = saw_odd_edges

        return compressed_grid

    def _build_prefix_sum(self) -> Grid:
        prefix_sum = Grid.empty(self.height + 1, self.width + 1, 0)
        for row in range(1, self.height + 1):
            for col in range(1, self.width + 1):
                prefix_sum[row, col] = (
                    prefix_sum[row - 1, col]
                    + prefix_sum[row, col - 1]
                    - prefix_sum[row - 1, col - 1]
                    + self.compressed_grid[row - 1, col - 1]
                )
        return prefix_sum


def part_1(points: list[Point]) -> int:
    return max(rectangle_area(p1, p2) for p1, p2 in it.combinations(points, 2))


def part_2(points: list[Point]) -> int:
    polygon = CompressedPolygon(points)

    # polygon.print_compressed_grid()

    best = 0
    for p1, p2 in it.combinations(points, 2):
        if polygon.is_filled(p1, p2):
            best = max(best, rectangle_area(p1, p2))
    return best


def main():
    data = get_data(year=2025, day=9, sample=False)
    points = [Point(*map(int, x.split(","))) for x in data.splitlines()]

    print("Part 1:", part_1(points))
    print("Part 2:", part_2(points))


if __name__ == "__main__":
    time_it(main)
