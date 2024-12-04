from common.data import *
from common.point import *


def parse_data(input):
    lines = input.splitlines()
    return lines


def part_1(grid):
    n = len(grid)
    m = len(grid[0])

    total = 0
    for i in range(n):
        for j in range(m):
            for dir in [LEFT, DOWN, DOWN_LEFT, DOWN_RIGHT]:
                indexes = [Point(i, j) + dir * x for x in range(4)]
                if all(p.is_valid_index(n, m) for p in indexes):
                    word = "".join([grid[p.i][p.j] for p in indexes])
                    total += word == "XMAS" or word == "SAMX"
    return total


def part_2(grid):
    n = len(grid)
    m = len(grid[0])

    total = 0
    for i in range(n):
        for j in range(m):
            offsets = [Point(0, 0), Point(0, 2), Point(1, 1), Point(2, 0), Point(2, 2)]
            indexes = [Point(i, j) + offset for offset in offsets]
            if all(p.is_valid_index(n, m) for p in indexes):
                word = "".join([grid[p.i][p.j] for p in indexes])
                total += word in ["MSAMS", "SSAMM", "MMASS", "SMASM"]

    return total


def main():
    input = get_data(year=2024, day=4, sample=False)
    print(f"Part 1: {part_1(parse_data(input))}")
    print(f"Part 2: {part_2(parse_data(input))}")


if __name__ == "__main__":
    main()
